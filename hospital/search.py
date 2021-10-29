from hospital.models import User
from sqlalchemy import or_


def search(query):
    
    results=User.query.filter(or_(User.email==query,User.apellidos==query,User.documento==query, User.nombres==query))
    dict_results={}

    lista=[]

    for i in results:
        
        nombres=i.nombres
        apellidos=i.apellidos
        documento=i.documento
        email=i.email
        id=str(i.id)
        lista_temp=[apellidos,nombres,documento,email,id]
        lista.append(lista_temp)


    return lista