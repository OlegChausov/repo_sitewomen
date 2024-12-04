from django.urls import path, re_path, register_converter
from . import views
from . import converters
from .views import WomenCategory

register_converter(converters.FourDigitYearConverter, "year4")

urlpatterns = [
    #path('', views.index, name='home'), #127.0.0.1:8000 name = алиас маршрута
    #path('about/', views.about, name='about'),
    #path('cats/<int:cat_id>/', views.categories, name='cats_id'), #127.0.0.1:8000/cats/cat_id
    #path('cats/<slug:cat_slug>/', views.categories_by_slug, name='cats'), #127.0.0.1:8000/cats/cat_id
    #re_path(r'^archive/(?P<year>[0-9]{4})/', views.archive, name='archive'), #127.0.0.1:8000/archive????
    #path('archive/<year4:year>/', views.archive, name='archive'), #127.0.0.1:8000/archive???? то же с помощью конвертера 'year4'
    #path('', views.index, name='home'),
    path('', views.WomenHome.as_view(), name='home'),#'при вызове можно переопределить переменную extra_context, которая была объявлена при объявлении класса и передать при вызове объекта класса WomenHome.as_view(extra_context={'title': "Главная страница сайта"})
    path('about/', views.about, name='about'),
    #path('addpage/', views.addpage, name='add_page'), # через функцию
    path('addpage/', views.AddPage.as_view(), name='add_page'),# через класс
    path('contact/', views.contact, name='contact'),
    path('login/', views.login, name='login'),
    #path('post/<int:post_id>/', views.show_post, name='post'), # маршрут с показом статей
    #path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    #path('cats/<int:cat_id>/', views.show_category, name='category'), категории по номерам
    #path('cats/<slug:cat_slug>/', views.show_category, name='category'),
    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
    #path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag',
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'
         )


]