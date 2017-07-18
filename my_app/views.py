from django.shortcuts import render
from my_app.forms import CreateUserForm, UserLogin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.forms import ValidationError
# Create your views here.


def index(request):
    return render(request, 'my_app/index.html')


def register(request):

    if request.method == "POST":
        create_user_form = CreateUserForm(data=request.POST)

        if create_user_form.is_valid():
            user = create_user_form.save()
            user.set_password(user.password)
            user.save()
            return index(request)

    else:
        create_user_form = CreateUserForm
    return render(request, 'my_app/registration.html', {'create_user_form': create_user_form})


def login_success(request, username):
    return render(request, 'my_app/succes.html', {'username': username})


def logout_success(request, username):
    return render(request, 'my_app/logout_success.html', {'username': username})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return login_success(request, user.username)
            else:
                form = UserLogin
                error = 'User is not Active'
                return render(request, 'my_app/login.html', {'form': form, 'error': error})
        else:
            form = UserLogin
            error = 'Username or Password not Correct'
            return render(request, 'my_app/login.html', {'form': form, 'error': error})
    else:
        form = UserLogin
        return render(request, 'my_app/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return index(request)