from hospital.models import User
from sqlalchemy import or_

def search(criterio):

    usuarios=User.query.filter(or_(User.nombres==criterio,User.apellidos==criterio,User.documento==criterio))
    
    return usuarios