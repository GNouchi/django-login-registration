from django.shortcuts import render, redirect 
from django.contrib import messages
from .models import *

def index(request):
    return render(request, 'index.html')

def login(request):
    if request.method == 'POST':
        print("-----------------------------at LOGIN----------------------------")
        result = User.objects.LoginValidator(request.POST)
        if len(result['errors']) > 0:
            print("errors are  : ",  result['errors'])
            for error in result['errors']:
                messages.error(request, error)
            return redirect('/')
        else:
            request.session['user_id']  = result['user_id']
            request.session['instance'] = 'login'
            return redirect('/success')
    else:
        return redirect('/')
    return redirect('/')

def register(request):
    if request.method == 'POST':
        print("-----------------------------at REGISTER----------------------------")
        result = User.objects.validateUser(request.POST)
        if len(result['errors']) > 0:
            print("errors are  : ",  result['errors'])
            for error in result['errors']:
                messages.error(request, error)
            return redirect('/')
        else:
            request.session['user_id']  = result['user_id']
            request.session['instance'] = 'registration'
            return redirect('/success')
    else:
        return redirect('/')


def success(request):
    if 'user_id' not in request.session or 'instance' not in request.session:
        return redirect ('/')
    current_user=User.objects.get(id = request.session['user_id'])
    if request.session['instance'] == 'registration' :
        dis = "Welcome newly Registered User!"
    elif request.session['instance'] == 'login':
        dis = "Welcome back old registered user"
    context=  {
        'current_user':  current_user,
        'instance' : dis
    }
    return render(request, 'success.html', context)

# user1@user1.user1
# user2@user2.user2
# user3@user3.user3