from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from authentication.models import CustomUser


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']

        user = CustomUser.create(email=email, password=password, first_name=username)
        user.role = int(role)
        user.save()
        return redirect('login')
        
    return render(request, 'authentication/register.html', {})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = CustomUser.get_by_email(email=email)
        if user and user.check_password(password):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('book_list')
    return render(request, 'authentication/login.html', {})
        
def logout_view(request):
    logout(request)
    return redirect('/auth/login/')

def book_list(request):
    return render(request, 'authentication/book_list.html', {})

def user_list(request):
    users = CustomUser.get_all()
    return render(request, 'authentication/user_list.html', {'users': users})
    
def user_detail(request, user_id):
    user = CustomUser.get_by_id(user_id)
    return render(request, 'authentication/user_detail.html', {'user': user})