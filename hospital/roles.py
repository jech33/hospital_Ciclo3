from flask import render_template

def roles(rol):
    if rol==0:
        return render_template('dashboard.html') #,nombres=nombres, apellidos=apellidos)
    if rol==2:
        return render_template('dashboard_usuario.html')