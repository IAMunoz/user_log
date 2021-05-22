from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.http import JsonResponse

import bcrypt

def index(request):
    if 'logged_user' in request.session:
        print('user: ', request.session['logged_user'])
        context = {
                'user' : request.session['logged_user']
            }
        return render(request, 'index.html', context)
    else: return render(request, 'index.html')

def register_user(request):
    if request.method == 'GET':
        #Si funciona, debe mostrar mensaje de registro existoso, y puede hacer login
        if request.session['logged_user']:
            print('registered user: ', request.session['logged_user'])
            context = {
                'user_reg' : request.session['logged_user']
            }
        return render(request, 'index.html', context)
    else:
        errors = User.objects.basic_validator(request.POST)
        if len(errors) >0:
            for k, v in errors.items():
                messages.error(request, v)
            return redirect('/')

        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print (pw_hash)
        user = User.objects.create(
            name = request.POST['name'], 
            password = pw_hash.decode(),
            lastname = request.POST['lastname'],
            email = request.POST['email']
        )
        request.session['logged_user'] = user.name
        return redirect("/register") 

def login_user(request):
    if request.method == 'GET':
        context = {
                'user_reg' : request.session['logged_user']
            }
        return render(request, 'success.html', context)
    else:
        
        results = User.objects.filter(email=request.POST['email'])
        print('user: ' , results)
        # Revisa si el usuario existe results es true
        if results:
            logged_user = results[0].email
            print('logged_email: ', logged_user)
            if bcrypt.checkpw(request.POST['password'].encode(), results[0].password.encode()):
                request.session['logged_user'] = results[0].name   
                return redirect("/login")
            else:
                messages.error(request, f"Contraseña no corresponde al usuario: {logged_user}")
                return redirect('/')
        else: 
            print('Usuario no encontrado')
            messages.error(request, 'Usuario no encontrado')
            return redirect('/')

def logout(request):
    try:
        del request.session['logged_user']
    except:
        print('Error')
    return redirect("/")    


def checkEmail(request):
    print("****** Validando Email ******")
    error = User.objects.checkEmail(request.POST["email"])
    print ('error: ', error.get('email'))
    #return redirect('/register')
    return JsonResponse({'error': error.get('email')})     
