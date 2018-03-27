from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.db import models
from time import gmtime, strftime
from datetime import datetime
from .models import User, UserManager
from .models import bcrypt, re

def index(request):
    return render(request, 'login/index.html')

def register(request):
    date = datetime.now().strftime('%Y-%m-%d')
    response = User.objects.validate_registration(request.POST, date)
    if response['status'] == True:
        request.session['user_id'] = response['user_id']
        request.session['name'] = response['name']
    else:
        for error in response['errors']:
            messages.error(request, error)
        return redirect('/')
    return redirect('/travels')

def login(request):
    response = User.objects.validate_login(request.POST)
    if response['status'] == True:
        request.session['user_id'] = response['user_id']
        request.session['name'] = response['name']
        print(User.name)
        # messages.info(request, info)
    else:
        for error in response['errors']:
            messages.error(request, error)
        return redirect('/')
    return redirect('/travels')


def logout(request):
    request.session.clear()
    return redirect('/')