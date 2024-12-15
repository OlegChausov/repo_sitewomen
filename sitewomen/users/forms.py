from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm): #наследуем для того, чтобы в классе представления LoginUser(LoginView) можно было использовать, иначем свою форму нельзя
    #след. атрибуты нужны только для указания своего label и widget
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = get_user_model() #Это рекомендуемая практика на случай изменения модели. Тогда в программе ничего дополнительно менять не придется.
        fields = ['username', 'password']