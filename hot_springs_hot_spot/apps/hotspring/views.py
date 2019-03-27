from django.shortcuts import render, redirect, HttpResponse
import bcrypt
from .models import User
from django.contrib import messages

def index(request):           
    if request.method == "GET":
        return render(request, 'hotspring/index.html', {"user" : User.objects.all()})
    if request.method == "POST":
        
        errors = User.objects.basic_validator(request.POST)
        if len(errors) > 0:
        #check if the dictionary contains any errors
        #if there are errors...
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            pw_hash = bcrypt.hashpw(request.POST["pword"].encode(), bcrypt.gensalt())
            new_user = User.objects.create(first_name=request.POST['fname'],last_name=request.POST['lname'], email=request.POST['email'], password=pw_hash)
            request.session['id'] = new_user.id
            return redirect("/home")

def username(request):
    # if request.method == "POST":
        context = {
            "found" : False
        }
        res = User.objects.filter(email =request.GET.get('email', ""))
        if len(res) > 0:
            context['found'] = True
            #ajax email verificar
        return render(request, "hotspring/username.html", context)

def home(request):
    if 'id' not in request.session:
        return redirect("/")
    else:   
        if request.method == 'GET':
            current_user = User.objects.get(id=request.session['id'])
            context ={
                "user" : current_user
            }
            return render (request, 'hotspring/home.html', context)

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            user = User.objects.get(email=request.POST['email'])
            request.session['id'] = user.id
            return redirect ("/home")

def logout(request):
    request.session.clear()
    return redirect ("/")

def homepage (request):
    return render(request, 'hotspring/home.html')

def find(request):
        return render (request, 'hotspring/find.html')

def community(request):
    return render(request, 'hotspring/community.html')

def news(request):
    return render(request, 'hotspring/news.html')

def about_me(request):
    return render(request, 'hotspring/about_me.html')