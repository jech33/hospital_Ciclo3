from operator import or_
import bcrypt
from flask.helpers import flash
from flask_wtf import form
from sqlalchemy.orm import query
from sqlalchemy.sql.elements import RollbackToSavepointClause
from sqlalchemy.sql.expression import null
from hospital import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request, session
from hospital.models import User
from hospital.models import Citas
from hospital.forms import CitasForm, RegisterForm, LoginForm, Busqueda
from hospital import db, bcrypt
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_
from hospital.roles import roles





@app.route('/', methods=['GET','POST'])
def inicio():
    if current_user.is_authenticated:
        print('Autenticado')
    else:
        print('No autenticado')
    return render_template('index.html')
    


@app.route('/contacto', methods=['GET','POST'])
def contacto():
    return render_template('contacto.html')


@app.route('/registro', methods=['GET','POST'])
def register_page():


    form = RegisterForm()

    if form.validate_on_submit():
        user_to_create = User(
            nombres= form.nombres.data,
            apellidos= form.apellidos.data,
            email= form.email.data,
            documento= form.documento.data,
            rol= 2,
            password_secure= form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f'Usuario creado exitosamente. Por favor ingrese.', category='succes')
        return redirect(url_for('Login'))

    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'Hubo un error creando al usuario: {err_msg}', category='danger')

    return render_template('registro.html', form=form)

@app.route('/conocenos', methods=['GET'])
def conocenos():
    return render_template('Conocenos.html')

    


    

@app.route('/login', methods = ['GET','POST'])
def Login():

    login_form=LoginForm()
    
    if login_form.validate_on_submit():
        attempted_user = User.query.filter_by(documento=login_form.documento.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=login_form.password.data):
            login_user(attempted_user)
            flash(f'Ingreso exitoso como: {attempted_user.apellidos}, {attempted_user.nombres}', category='success')
            return redirect(url_for('dashboard'))
        else:
            flash('El documento y la contraseña no coinciden. Por favor intente de nuevo', category='danger')
  
    return  render_template("/login.html", login_form=login_form)


@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    return roles(current_user.rol)







@app.route('/logout')
def logout_page():
    logout_user()
    flash('Se ha cerrado la sesión', category='info')
    return redirect(url_for('inicio'))



@app.route('/citas', methods=['GET','POST'])
@login_required
def citas():
    citas_form=CitasForm()
    user_paciente=current_user.apellidos+' '+current_user.nombres

    if citas_form.validate_on_submit():
        print(user_paciente)
        cita_a_crear = Citas(paciente=user_paciente,
                            medico=citas_form.medico.data, 
                            fecha=citas_form.fecha.data,
                            hora=citas_form.hora.data)
        db.session.add(cita_a_crear)
        db.session.commit()
        flash('Cita agendada exitosamente', category='success')
        return redirect(url_for('dashboard'))

    return render_template('citas.html', citas_form=citas_form )



@app.route('/busqueda_usuario', methods=['GET','POST'])
@login_required
def busqueda_usuario():

    usuarios = User.query.filter().all()
    if request.method == 'POST' and 'query' in request.form:
        tag = request.form['query']
        seek = "{}%".format(tag)
        usuarios = User.query.filter(or_(User.nombres.like(seek), 
            User.apellidos.like(seek),
            User.documento.like(seek),
            User.email.like(seek),
            User.id.like(seek))).all()
        list_lenght=len(usuarios)
        total_length=len(User.query.all())
            
        return render_template('busqueda_usuario.html', results=usuarios, query=tag, length=list_lenght, total_length=total_length)
    return render_template('busqueda_usuario.html', results=usuarios)


@app.route('/busqueda_citas', methods=['GET','POST'])
@login_required
def busqueda_citas():

    citas = Citas.query.filter().all()
    if request.method == 'POST' and 'query_paciente' in request.form:
        tag_paciente = request.form['query_paciente']
        tag_medico = request.form['query_medico']
        tag_fecha = request.form['query_fecha']
        print(tag_paciente,tag_medico,tag_fecha)
        seek = ["{}%".format(tag_paciente),"{}%".format(tag_medico), "{}%".format(tag_fecha)]
        citas = Citas.query.filter(Citas.paciente.like(seek[0]), 
                                    Citas.medico.like(seek[1]),
                                    Citas.fecha.like(seek[2])).all()
        list_lenght=len(citas)
        total_length=len(Citas.query.all())
            
        return render_template('busqueda_citas.html', results=citas, query_paciente=tag_paciente, query_medico=tag_medico, query_fecha=tag_fecha, length=list_lenght, total_length=total_length)
    return render_template('busqueda_citas.html', results=citas)


@app.route('/mis_citas')
@login_required
def mis_citas():
    paciente_a_buscar=current_user.apellidos+' '+current_user.nombres
    citas=Citas.query.filter_by(paciente=paciente_a_buscar).all()
    length=len(citas)
    return render_template('mis_citas.html', citas=citas,length=length)




@app.route('/borrar/<int:id>')
def delete(id):
    usuario_a_borrar=User.query.get_or_404(id)

    try:
        db.session.delete(usuario_a_borrar)
        db.session.commit()
        flash('Usuario eliminado exitosamente', category='success')
        return redirect('/busqueda_usuario')
    
    except:
        return "Hubo un error eliminando al usuario"

@app.route('/borrar_cita/<int:id>')
def delete_cita(id):
    cita_a_borrar=Citas.query.get_or_404(id)

    try:
        db.session.delete(cita_a_borrar)
        db.session.commit()
        flash('Cita eliminada exitosamente', category='success')
        return redirect('/busqueda_citas')
    
    except:
        return "Hubo un error eliminando la cita"

@app.route('/borrar_mi_cita/<int:id>')
def delete_mi_cita(id):
    cita_a_borrar=Citas.query.get_or_404(id)

    try:
        db.session.delete(cita_a_borrar)
        db.session.commit()
        flash('Cita eliminada exitosamente', category='success')
        return redirect('/mis_citas')
    
    except:
        return "Hubo un error eliminando la cita"



@app.route('/Quienes_Somos', methods=['GET','POST'])
def quienesSomos():
    return render_template('Quienes_Somos.html')

@app.route('/PQR', methods=['GET','POST'])
def pqr():
    return render_template('PQR.html')

@app.route('/FAQ', methods=['GET'])
def faq():
    return render_template('FAQ.html')




@app.route('/perfil_paciente', methods = ["GET"])
def pacientee():
    return  render_template("/Perfil_pacientes.html")



@app.route('/perfil_paciente/comentarios', methods = ["GET","POST"])
def Comentarios():
    return  "Preguntas Comentarios"
# Crear comentarios y ver comentarios 

@app.route('/perfil_paciente/Datos_personales', methods = ["GET"])
def Datos_personales():
    return  " Datos personales   "
# Crear opcion para actualizar 

@app.route('/perfil_medico', methods = ["GET"])
def Medico():
    return  render_template("/Medico.html")

@app.route('/perfil_medico/historia_medica', methods = ["GET","POST"])
def Historia_medica():
    return  "Pagina de Historia Medica "
#Consultar, actualizar y el resto

@app.route('/perfil_medico/citas', methods = ["GET","POST"])
def Citas_1():
    return  "Pagina de Citas "
# Modificar y eliminar 

@app.route('/perfil_medico/Datos_personales', methods = ["GET"])
def Datos_personales_1():
    return  " Datos personales  "
#actualizar 

@app.route('/perfil_superadministrativo', methods = ["GET"])
def superadministrativo () :
    return render_template("/superadmin.html")

@app.route('/perfil_superadministrativo/historia_medica', methods = ["GET","POST"])
def Historia_medica_1():
    return  "Pagina de Historia Medica "
#Crear, consultar, actualizar 

@app.route('/perfil_superadministrativo/usuarios', methods = ["GET","POST"])
def Usuarios_9():
    return render_template("/superadmin_usuarios.html")
    #Crear usuario

@app.route('/perfil_superadministrativo/usuarios/consultar', methods = ["GET","POST"])
def Consultar_9():
    return render_template("/super_admin_consultar.html")

@app.route('/perfil_superadministrativo/usuarios/consultar/editar', methods = ["GET","POST"])
def editar_2():
    return render_template("/superadmin_editar_usuario.html")
#eliminar, editar

@app.route('/perfil_superadministrativo/citas', methods = ["GET","POST"])
def Citas_4():
    return  "Pagina de Citas "
#crear, eliminar, editar 

