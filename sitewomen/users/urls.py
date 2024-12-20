from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    #path('logout/', LogoutView.as_view(), name='logout', #в джанго 5 уже нельзя!!! В джанго 5 запрещен логаут по гет-запросу),
    #path('register/', views.register, name='register'),
    path('password-change/', views.UserPasswordChange.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="users/password_change_done.html"), name="password_change_done"),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('register/', views.RegisterUser.as_view(), name='register'),
]
#если реализовывать функциями, а не классами
# path('logout/', views.login_user, name='login')
# path('logout/', views.logout_user, name='logout')