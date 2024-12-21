from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import LoginUserForm, RegisterUserForm, ProfileUserForm, UserPasswordChangeForm


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

# def register(request):
#     if request.method == "POST":
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)  # создание объекта без сохранения в БД
#             user.set_password(form.cleaned_data['password']) #шифруем пароль и заносим в модель
#             user.save()
#             return render(request, 'users/register_done.html')
#     else:
#         form = RegisterUserForm()
#     return render(request, 'users/register.html', {'form': form})

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': "Регистрация"}
    success_url = reverse_lazy('users:login')


class ProfileUser(LoginRequiredMixin, UpdateView): #UpdateView берет на себя функционал по изменению данных в профиле пользователя
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}

    def get_success_url(self):
        return reverse_lazy('users:profile')

    #профайл будет открываться только для текущего пользователя, либо сделано перенаправление на страницу авторизации для неавторизованных пользователей:
    def get_object(self, queryset=None):
        return self.request.user

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("users:password_change_done")
    template_name = "users/password_change_form.html"
    extra_context = {'title': "Изменение пароля"}