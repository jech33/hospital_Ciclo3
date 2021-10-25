from enum import unique
from hospital import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    nombres = db.Column(db.String(length=30), nullable=False)
    apellidos = db.Column(db.String(length=30), nullable=False)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    documento = db.Column(db.String(length=20), nullable=False, unique=True)
    password = db.Column(db.String(length=60), nullable=False)


class Citas(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    paciente=db.Column(db.String(length=50), nullable=False)
    medico=db.Column(db.String(length=50), nullable=False)
    fecha=db.Column(db.String(length=50), nullable=False)
    hora=db.Column(db.String(length=50), nullable=False)
    comentarios=db.Column(db.String(length=50), nullable=True)
    calificacion=db.Column(db.Integer(), nullable=True)



    
