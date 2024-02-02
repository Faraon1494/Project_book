from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import NewUserForm, UserChangeForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def user_register(request):
    if request.method == "POST":
        print("register equal")
        register_form = NewUserForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            print("register is valid")
            return redirect('main:index')
    register_form = NewUserForm
    print("register render")
    return render(request=request, template_name='user_auth/register.html', context={'register_form': register_form})

def user_login(request):
    if request.method == "POST":
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('main:index')
    
    login_form = AuthenticationForm()
    return render(request=request, template_name='user_auth/login.html', context={'login_form': login_form})

def user_logout(request):
    logout(request)
    return redirect('main:index')

def user_cab(request):
    username = None

    if request.user.is_authenticated:
        username = request.user.username
    return render(request, 'user_auth/cab.html')


# код для обновления username.
def change_user_data(request):
    text_value = None
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST)
        if user_form.is_valid():
            text_value = user_form.cleaned_data['text_input']
            owner = request.user
            owner.username = text_value
            owner.save() 
    else:
        user_form = UserChangeForm()

    return render(request, 'user_auth/cab.html', {'user_form': user_form, 'text_value': text_value})