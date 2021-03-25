from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User
from .models import Message
from .models import Comment
import bcrypt


def index(request):
    # if 'id' in request.session.keys():
    #     return redirect('/success')
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
    
    context = {
        'all_messages': Message.objects.all()
    }
    return render(request, 'wall.html', context)

def logout(request):
    request.session.clear()  
    return redirect('/')

def post_message(request):
    Message.objects.create(
        content = request.POST['message'],
        user = User.objects.get(id = request.session['user_id'])
    )
    return redirect('/success')

def post_comment(request):
    Comment.objects.create(
        user = User.objects.get(id = request.session['user_id']),
        content = request.POST['comment'],
        message = Message.objects.get(id = request.POST['message_id']),
    )
    return redirect('/success')

def delete_message(request):
    message = Message.objects.get(id = request.POST['message_id'])
    message.delete()
    return redirect('/success')

def delete_comment(request):
    comment = Comment.objects.get(id = request.POST['comment_id'])
    comment.delete()
    return redirect('/success')

# create function with context for all_users:User.objects.all()

# context is key/value pairs.  keys are how the front end accesses the data stored in values
# context must be passed in the return statement

