from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    #path('logout/', LogoutView.as_view(), name='logout', #в джанго 5 уже нельзя!!! В джанго 5 запрещен логаут по гет-запросу),
    path('register/', views.register, name='register'),
]
#если реализовывать функциями, а не классами
# path('logout/', views.login_user, name='login')
# path('logout/', views.logout_user, name='logout')