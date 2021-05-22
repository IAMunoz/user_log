from __future__ import unicode_literals
from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):    
        errors = {}
        # agregue claves y valores al diccionario de errores para cada campo no válido
        if len(postData['name']) < 2:
            errors["name"] = "El nombre debe tener mas de 2 caracteres"
        if len(postData['lastname']) < 2:
            errors["lastname"] = "El apellido debe tener mas de 2 caracteres"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData["email"]):          
            errors['email'] = "Correo Invalido"
        m = User.objects.filter(email=postData["email"])
        if m :
            errors['user'] = f"Correo {m[0].email} ya esta registrado"
        if len(postData['password']) < 4:
            errors["pass1"] = "El password debe tener mas de 4 caracteres"
        if not re.search('[0-9]',postData['password']):
            errors["pass2"] = "El password debe tener al menos un numero"
        if postData['check'] != postData['password'] :
            errors["password"] = "Los Password no coinciden"
        return errors      

    def checkEmail(self, data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(data):          
            errors['email'] = "Correo Invalido"
        return errors      

# MIN_FIELD_LENGTH = 4
# def ValidarLongitudMinima(cadena):
#     if len(cadena) < MIN_FIELD_LENGTH:
#         raise 

# def ValidarEmail():
    
class User(models.Model):
    name = models.CharField(max_length=45, blank = False, null =False)
    lastname = models.CharField(max_length=45, blank = True, null =True)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()          
