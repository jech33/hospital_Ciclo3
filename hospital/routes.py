import bcrypt
from flask.helpers import flash
from flask_wtf import form
from hospital import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from hospital.models import Citas, User
from hospital.forms import CitasForm, RegisterForm, LoginForm
from hospital import db, bcrypt
from flask_login import login_user


@app.route('/')
@app.route('/', methods=['GET','POST'])
def inicio():
    print('hola')
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
            password_secure= form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('inicio'))

    if form.errors !={}:
        for err_msg in form.errors.values():
            flash(f'Hubo un error creando al usuario: {err_msg}')

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
def dashboard():
    return render_template('dashboard.html')




@app.route('/citas', methods=['GET','POST'])
def citas():
    citas_form=CitasForm()
    if citas_form.validate_on_submit():
        cita_a_crear = Citas(paciente=citas_form.paciente.data,
                            medico=citas_form.medico.data,
                            fecha=citas_form.fecha.data,
                            hora=citas_form.hora.data)
        db.session.add(cita_a_crear)
        db.session.commit()
        return redirect(url_for('inicio'))

    return render_template('citas.html', citas_form=citas_form )

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
def Paciente():
    return  render_template("/Perfil_pacientes.html")

@app.route('/perfil_paciente/citas', methods = ["GET","POST"])
def Citas():
    return  render_template("/Citas.html")
#Crear hmtl para crear, y consultar, ver citas 

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