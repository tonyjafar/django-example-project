from django.shortcuts import render
from my_app.forms import CreateUserForm, UserLogin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
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


@login_required
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


class UsersListView(ListView):
    context_object_name = 'users_list'
    model = User
    template_name = 'my_app/user_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UsersListView, self).dispatch(request, *args, **kwargs)


class UserDetailView(DetailView):
    context_object_name = 'user_details'
    model = User
    template_name = 'auth/user_detail.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserDetailView, self).dispatch(request, *args, **kwargs)


class UserUpdateView(UpdateView):
    fields = ("username", "email")
    model = User
    success_url = reverse_lazy("my_app:users_list")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy("my_app:users_list")

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request, *args, **kwargs)