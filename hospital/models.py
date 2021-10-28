from enum import unique
from hospital import db , login_manager
from hospital import bcrypt
from flask_login import UserMixin





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    nombres = db.Column(db.String(length=30), nullable=False)
    apellidos = db.Column(db.String(length=30), nullable=False)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    documento = db.Column(db.String(length=20), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)

    @property
    def password_secure(self):
        return self.password_secure

    @password_secure.setter
    def password_secure(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')


    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password) 


class Citas(db.Model):
    
    id = db.Column(db.Integer(), primary_key=True)
    paciente=db.Column(db.String(length=50), nullable=False)
    medico=db.Column(db.String(length=50), nullable=False)
    fecha=db.Column(db.String(length=50), nullable=False)
    hora=db.Column(db.String(length=50), nullable=False)
    comentarios=db.Column(db.String(length=50), nullable=True)
    calificacion=db.Column(db.Integer(), nullable=True)




    
