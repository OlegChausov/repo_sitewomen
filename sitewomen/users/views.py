from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from users.forms import LoginUserForm, RegisterUserForm


# def login_user(request):
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password']) #authenticate проверяет в БД пользователя со значениями по ключам 'username', 'password'
#             if user and user.is_active:
#                 login(request, user) #авторизация. создается сессия, туда заносится информация
#                 return HttpResponseRedirect(reverse('home'))
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/login.html', {'form': form})

class LoginUser(LoginView):
   #form_class = AuthenticationForm #LoginUserForm не подходит, т.к. для калсса LoginView определена форма AuthenticationForm, но можно изменить
   form_class = LoginUserForm  # Можно если class LoginUserForm(AuthenticationForm)
   template_name = 'users/login.html'
   extra_context = {'title': "Авторизация"}
   # по умолчанию редиректит на http://127.0.0.1:8000/accounts/profile/, но это поменяем переопределив:
   def get_success_url(self):
       return reverse_lazy('home')
    #приоритеты автоперенаправления после логина: 1 - get_success_url; login.html/{{ next }}; 3 - settings.py/LOGIN_REDIRECT_URL ; 4 - url..accounts/profile
#     или можно в settings.py указать
#LOGIN_REDIRECT_URL = '/' или например так LOGIN_REDIRECT_URL = 'home' - сюда перенапрвлять
#LOGIN_REDIRECT_URL – задает URL-адрес, на который следует перенаправлять пользователя после успешной авторизации;
#LOGIN_URL – определяет URL-адрес, на который следует перенаправить неавторизованного пользователя при попытке посетить закрытую страницу сайта;
#LOGOUT_REDIRECT_URL – задает URL-адрес, на который перенаправляется пользователь после выхода.



def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))#чтоб не перепуталь с women/login

def register(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # создание объекта без сохранения в БД
            user.set_password(form.cleaned_data['password']) #шифруем пароль и заносим в модель
            user.save()
            return render(request, 'users/register_done.html')
    else:
        form = RegisterUserForm()
    return render(request, 'users/register.html', {'form': form})
