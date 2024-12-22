from django.contrib.auth.views import LogoutView, PasswordChangeView, PasswordChangeDoneView, PasswordResetDoneView, \
    PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import path, reverse_lazy
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
    path('password-reset/',
         PasswordResetView.as_view(
             template_name="users/password_reset_form.html",
             email_template_name="users/password_reset_email.html",
             success_url=reverse_lazy("users:password_reset_done")
         ),
         name='password_reset'), #явно укажем свой шаблон, а не дефолтный
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name = "users/password_reset_done.html"), name='password_reset_done'), #явно укажем свой шаблон, а не дефолтный
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="users/password_reset_confirm.html",
             success_url=reverse_lazy("users:password_reset_complete")), name='password_reset_confirm'),
    path('password-reset/complete/', PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name='password_reset_complete'), #явно укажем свой шаблон, а не дефолтный
]
#если реализовывать функциями, а не классами
# path('logout/', views.login_user, name='login')
# path('logout/', views.logout_user, name='logout')