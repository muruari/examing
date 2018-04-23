from __future__ import unicode_literals
import bcrypt, time
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from datetime import datetime

def current_user(request):
	return User.objects.get(id = request.session['user_id'])


def registration(request):
	return render(request, 'exam/registration.html')


def register(request):
    check = User.objects.validate(request.POST)
    if request.method != 'POST':
		return redirect('/')
    if len(check) > 0:
        for error in check:
            messages.add_message(request, messages.INFO, error, extra_tags="register")
            return redirect('/')

    passwd = request.POST['password']
    if len(check) == 0:
		hashed_pw = bcrypt.hashpw(str(passwd).encode(), bcrypt.gensalt())

    #Creates a new user in the database:
    User.objects.create(
        name = request.POST['name'],
        alias = request.POST['alias'],
        email = request.POST['email'],
        password = hashed_pw,
        date_of_birth = request.POST['date_of_birth'],
    )

    user = User.objects.get(email = request.POST['email'])
    email = request.POST['email']
    request.session['user_id'] = user.id
    request.session['name'] = user.name
    return redirect('/dashboard')


def login(request):
    if request.method != 'POST':
        return redirect('/')
    user = User.objects.filter(email = request.POST.get('email')).first()
    if user and bcrypt.checkpw(request.POST.get('password').encode(), user.password.encode()):
        request.session['user_id'] = user.id
        request.session['name'] = user.name
        return redirect('/dashboard')
    else: 
        messages.add_message(request, messages.INFO, 'Your login credentials are invalid! Please try again.', extra_tags="login")
        return redirect('/')
    return redirect('/dashboard')

	

def logout(request):
		request.session.clear()
		return redirect('/')


def dashboard(request):
    user = User.objects.get(id = request.session['user_id'])
    
    all_users = User.objects.filter()
    my_friends = Friend.objects.filter(friended_by = user)
    context = {
        'user' : user,
        'my_friends' : my_friends,
        'all_users' : all_users
    }
    return render(request, 'exam/dashboard.html', context)


def add_friend(request, id):
    user = User.objects.get(id = request.session['user_id'])
    friend = User.objects.get (id = id)
    Friend.objects.create(users = user, friended_by = friend)
    Friend.objects.create(users = friend, friended_by = user)
    return redirect('/dashboard')


def remove_friend(request, id):
    user = User.objects.get(id = request.session['user_id'])
    friend = User.objects.get (id = id)
    first_friend = Friend.objects.get(users = user, friended_by = friend)
    second_friend = Friend.objects.get(users = friend, friended_by = user)
    first_friend.delete()
    second_friend.delete()
    return redirect('/dashboard')


def user_page(request, id):
    user = User.objects.get(id = id)
    context = {
        'user' : user
    }
    return render(request, 'exam/user.html', context)

