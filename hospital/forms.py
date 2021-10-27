from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.core import DateField, IntegerField, SelectField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from hospital.models import User

lista_medicos=['Medico 1','Medico 2','Medico 3']
lista_horas=['8:00 AM - 9:00 AM', '9:00 AM - 10:00 AM','10:00 AM - 11:00 AM','11:00 AM - 12:00 PM','12:00 PM - 1:00 PM','1:00 PM - 2:00 PM','2:00 PM - 3:00 PM','3:00 PM - 4:00 PM','4:00 PM - 5:00 PM','5:00 PM - 6:00 PM']


class RegisterForm(FlaskForm):

    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('El correo ya se encuentra registrado')

            

    nombres=StringField(label='Nombres:',validators=[DataRequired()])
    apellidos=StringField(label='Apellidos',validators=[DataRequired()])
    email=StringField(label='Email:',validators=[Email(),DataRequired()])
    documento=StringField(label='Numero de documento:',validators=[DataRequired(),Length(min=6,max=20)])
    password1=PasswordField(label='Contraseña:',validators=[DataRequired(),Length(min=4)])
    password2=PasswordField(label='Confirme su contrasena:',validators=[DataRequired(),EqualTo('password1')])
    submit=SubmitField(label='CREAR CUENTA')

class CitasForm(FlaskForm):
    paciente=StringField(label='Nombre:',validators=[DataRequired()])
    #medico=StringField(label='Medico:')
    medico=SelectField('Escoja un medico',choices=lista_medicos, validators=[DataRequired()])
    fecha=StringField(label='Escoja el dia',validators=[DataRequired()])
    #hora=StringField(label='Escoja la hora')
    hora=SelectField('Escoja la hora',choices=lista_horas,validators=[DataRequired()])
    submit = SubmitField(label='Agendar cita')

class LoginForm(FlaskForm):
    documento=StringField(label='Su número de documento:', validators=[DataRequired()])
    password=PasswordField(label='Ingrese su contraseña:', validators=[DataRequired()])
    submit = SubmitField(label='Iniciar sesión')