from django.shortcuts import render, redirect
from .models import User, Destination
from django.contrib import messages
from time import gmtime, strftime
from datetime import datetime

def index(request):
    if 'user_id' not in request.session:
        return redirect ('/')
    context = {
        'User': User.objects.get(id=request.session['user_id']),
        'committed_plans': Destination.objects.filter(joiners=request.session['user_id']),
        'uncommitted_plans': Destination.objects.exclude(joiners=request.session['user_id'])
    }

    return render(request, 'travels/index.html', context)

def join(request):
    user = User.objects.get(id=request.session['user_id'])
    destination = Destination.objects.get(id=request.POST['destination_id'])
    destination.joiners.add(user)
    destination.save()
    
    return redirect('/travels')

def leave(request):
    user = User.objects.get(id=request.session['user_id'])
    plan = Destination.objects.get(id=request.POST['trip_id'])
    plan.joiners.delete(user)
    plan.save()
    
    return redirect('/travels')

def add(request):

    return render(request, 'travels/add.html')

def addtrip(request):
    print(request.POST)
    date = datetime.now().strftime('%Y-%m-%d')
    response = Destination.objects.validate_destination(request.POST, date, request.session['user_id'])
    if response['status'] == True:
        print ('redirecting to landing page')
    else:
        for error in response['errors']:
            messages.error(request, error)
        return redirect('/travels/add')
    return redirect('/travels')

def destination(request, id):
    context = {
        'Destination': Destination.objects.get(id=id)
    }
    return render (request, 'travels/destination.html', context)