from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.core import DateField, IntegerField, SelectField


lista_medicos=['Medico 1','Medico 2','Medico 3']
lista_horas=['8:00 AM - 9:00 AM', '9:00 AM - 10:00 AM','10:00 AM - 11:00 AM','11:00 AM - 12:00 PM','12:00 PM - 1:00 PM','1:00 PM - 2:00 PM','2:00 PM - 3:00 PM','3:00 PM - 4:00 PM','4:00 PM - 5:00 PM','5:00 PM - 6:00 PM']


class RegisterForm(FlaskForm):
    nombres = StringField(label='Nombres:')
    apellidos = StringField(label='Apellidos:')
    email = StringField(label='Correo electrónico:')
    documento = StringField(label='Su número de documento:')
    password1 = PasswordField(label='Contraseña:')
    password2 = PasswordField(label='Confirme su contraseña:')
    submit = SubmitField(label='CREAR CUENTA')

class CitasForm(FlaskForm):
    paciente=StringField(label='Nombre:')
    #medico=StringField(label='Medico:')
    medico=SelectField('Escoja un medico',choices=lista_medicos)
    fecha=StringField(label='Escoja el dia')
    #hora=StringField(label='Escoja la hora')
    hora=SelectField('Escoja la hora',choices=lista_horas)
    submit = SubmitField(label='Agendar cita')
    