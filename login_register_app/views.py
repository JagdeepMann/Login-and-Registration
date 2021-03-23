from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
import bcrypt


def index(request):
    return render(request, 'index.html')

def register_user(request):
    
    if request.method == 'GET':
        return redirect('/')
    
    errors = User.objects.validator(request.POST)
    if errors:
        # loop to iterate to get values in errors dictionary
        for val in errors.values():
            messages.error(request, val)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )
        messages.info(request, "Account successfully created! please log in!")
    
    return redirect('/') #**** can be redirected to /succuess

def authentication(request):
    
    try:
        user = User.objects.get(email = request.POST['email'])
    except:
        messages.error(request, "Incorrect login credentials")
        return redirect('/')
    
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['user_id'] = user.id
        request.session['user_first_name'] = user.first_name
        request.session['user_last_name'] = user.last_name
        request.session['user_email'] = user.email
        return redirect('/success')
    
    messages.error(request, "Incorrect login credentials")
    return redirect('/')

def success(request):
    if "user_id" not in request.session:
        messages.error(request, "please log in")
        return redirect('/')
    return render(request, 'success.html')

def logout(request):
    request.session.clear()
    # if 'user_id' in request.session:
    #     del request.session['user_id']
    # if 'user_first_name' in request.session:
    #     del request.session['user_id']
    # if 'user_last_name' in request.session:
    #     del request.session['user_id']
    # if 'user_email' in request.session:
    #     del request.session['user_id']   
    return redirect('/')