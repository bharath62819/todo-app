from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from todoapp import models
from todoapp.models import ToDo
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def signup(request):
    if request.method=='POST':
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        pwd = request.POST.get('pwd')
        my_user = User.objects.create_user(uname,email,pwd)
        my_user.save()
        return redirect('/login')
    return render(request,'todoapp/index.html')

def LogIn(request):
    if request.method=='POST':
        uname = request.POST.get('uname')
        pwd = request.POST.get('pwd')
        user = authenticate(request,username=uname,password=pwd)
        if user is not None:
            login(request,user)
            return redirect('/todo')
        else:
            return render(request, 'todoapp/login.html', {'error': 'Invalid credentials'})
    return render(request,'todoapp/login.html')

@login_required(login_url='/login')
def todo(request):
    if request.method=='POST':
        title = request.POST.get('title')
        obj = models.ToDo(title=title,user=request.user)
        obj.save()
        res= models.ToDo.objects.filter(user=request.user).order_by('-date')
        return redirect('/todo',{'res':res})
    res= models.ToDo.objects.filter(user=request.user).order_by('-date')
    return render(request,'todoapp/todo.html',{'res':res})

@login_required(login_url='/login')
def edit_todo(request,srno):
    if request.method=='POST':
        title = request.POST.get('title')
        obj = models.ToDo.objects.get(srno=srno)
        obj.title=title
        obj.save()
        return redirect('/todo')
    obj = models.ToDo.objects.get(srno=srno)
    return render(request,'todoapp/edit_todo.html',{'obj':obj})

@login_required(login_url='/login')
def delete_todo(request,srno):
    obj=models.ToDo.objects.get(srno=srno)
    obj.delete()
    return redirect('/todo')

def signout(request):
    logout(request)
    return redirect('/login')





