from django.shortcuts import render, redirect, HttpResponse
import bcrypt
from .models import User, Message, Comment, Hotspring
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
            all_hotsprings = Hotspring.objects.all().order_by("-updated_at")
            user = User.objects.get(id=request.session['id'])
            context ={
                "user" : user,
                "all_hot)springs" : all_hotsprings
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
            
    if request.method == 'POST':
        hot_spring = Hotspring.objects.create(name=request.POST['name'], city=request.POST['city'], state=request.POST['state'], country=request.POST['country'], comment=request.POST['comment'])
        my_val = hot_spring.id
        print("*********************************",my_val)
        return redirect("/view/"+str(my_val))
    else:
        return render (request, 'hotspring/find.html')

def community(request):
    if 'id' not in request.session:
        return redirect("/")
    else:   
        if request.method == 'GET':
            all_users = User.objects.all()
            all_messages = Message.objects.all()
            all_comments = Comment.objects.all() 
            all_hotsprings = Hotspring.objects.all().order_by("-updated_at")
            user = User.objects.get(id=request.session['id'])
            context ={
                "user" : user,
                "all_hotsprings" : all_hotsprings,
                "all_messages" : all_messages,
                "all_users" : all_users,
                "all_comments" : all_comments,
            }
            return render (request, 'hotspring/community.html', context)
        if request.method == 'POST':
            hot_spring = Hotspring.objects.create(name=request.POST['name'], city=request.POST['city'], state=request.POST['state'], country=request.POST['country'], comment=request.POST['comment'])
            my_val = hot_spring.id
            print("*********************************",my_val)
            return redirect("/view/"+str(my_val))
             

def delete_message(request, my_val):
    delete = Message.objects.get(id = my_val)
    delete.delete()
    return redirect("/community")

def delete_comment(request, my_val):
    delete = Comment.objects.get(id = my_val)
    delete.delete()
    return redirect("/community")

def news(request):
    return render(request, 'hotspring/news.html')

def about_me(request):
    return render(request, 'hotspring/about_me.html')

def view(request, my_val):
    if 'id' not in request.session:
        return redirect("/")
    else:   
        if request.method == 'GET':
            hotspring = Hotspring.objects.get(id=my_val)
            all_users = User.objects.all()
            all_messages = Message.objects.all()
            all_comments = Comment.objects.all()
            current_user = User.objects.get(id=request.session['id'])
            context={
                "hotspring" : hotspring,
                "current_user" : current_user,
                "all_messages" : all_messages,
                "all_users" : all_users,
                "all_comments" : all_comments
                }
            return render(request, 'hotspring/view.html', context)

def send_message(request):
    if request.method == "POST":
        print(request.session['id'])
        user = User.objects.get(id = request.session['id'])
        new_message = Message.objects.create(message=request.POST['message'], user = user,)
        print(new_message, "**********************")
        return redirect("/community")

def send_comment(request):
    if request.method == "POST":
        user = User.objects.get(id = request.session['id'])
        message = Message.objects.get(id = request.POST['message_id'] )
        comment = Comment.objects.create(comment=request.POST['comment'], user = user, message=message)
        print(message.comments,"***********************")
        return redirect("/community")

def edit(request, my_val):
    if 'id' not in request.session:
        return redirect("/")
    else:   
        if request.method == 'GET':
            current_user = User.objects.get(id=request.session['id'])
            hotspring = Hotspring.objects.get(id = my_val)
            context={
                "my_val":my_val,
                "current_user" : current_user,
                "hotspring" : hotspring
            }
            return render(request, "hotspring/edit.html" , context)
        if request.method == 'POST':
            hotspring = Hotspring.objects.get(id = my_val)
            print("*****************************************",hotspring)
            hotspring.name = request.POST['name']
            hotspring.city = request.POST['city']
            hotspring.state = request.POST['state']
            hotspring.country = request.POST['country']
            hotspring.comment = request.POST['comment']
            hotspring.save()
            return redirect ("/view/"+str(my_val))

def delete (request, my_val):
    hotspring_to_delete = Hotspring.objects.get(id = my_val)
    hotspring_to_delete.delete()
    return redirect("/community")