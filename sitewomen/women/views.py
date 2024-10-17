from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from .models import Women

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]
data_db = [
    {'id': 1, 'title': 'Анджелина Джоли', 'content': '''<p>Анджелина Джоли</p> (англ. Angelina Jolie[7], при рождении Войт (англ. Voight), ранее Джоли Питт (англ. Jolie Pitt); род. 4 июня 1975, Лос-Анджелес, Калифорния, США) — американская актриса кино, телевидения и озвучивания, кинорежиссёр, сценаристка, продюсер, фотомодель, посол доброй воли ООН.

Обладательница премии «Оскар», трёх премий «Золотой глобус» (первая актриса в истории, три года подряд выигравшая премию) и двух «Премий Гильдии киноактёров США».''',
     'is_published': True},
    {'id': 2, 'title': 'Марго Робби', 'content': 'Биография Марго Робби', 'is_published': False},
    {'id': 3, 'title': 'Джулия Робертс', 'content': 'Биография Джулия Робертс', 'is_published': True},
]

cats_db = [
    {'id': 1, 'name': 'Актрисы'},
    {'id': 2, 'name': 'Певицы'},
    {'id': 3, 'name': 'Спортсменки'},
]

def index(request):
    # posts = Women.objects.filter(is_published=1) это со старым дефолтным менеджером
    posts = Women.published.all()# all вместо filter потому, что этот менеджер возвращает только те записи, которые нужны, фильтровать не нужно

    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': posts,
       # 'cat_selected': 0,  # не обязательная строчка
    }
    return render(request, 'women/index.html', context=data)
    #return HttpResponse(render_to_string('women/index.html')) альтернативный вариаент

def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'women/post.html', context=data)

def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu})

#def categories(request, cat_id): #HttpRequest
#    return HttpResponse(f"<h1>Статьи по категориям</h1><p>id: {cat_id}</p>")

#def categories_by_slug(request, cat_slug):
#    if request.GET:
#        print(request.GET)
#    return HttpResponse(f"<h1>Статьи по категориям</h1><p>slug: {cat_slug}</p>")

#def archive(request, year):
#    if year>2024:
#        #return redirect('/', permanent=True) #перенаправление на новый адрес, в данном случае '/' главная страница, перманент - 301 код, постоянное
#        #return redirect(index, permanent=True)#аналогично можно с помощью функции, в данном случае функция index главная страница, перманент - 301 код, постоянное
#        #return redirect('home', permanent=True)#правильно использовать алиасы
#        #return redirect('cats', 'music')# 'cats' - маршрут по slug, music - его slug-параметр
#        uri=reverse('cats', 'music') # вычисляет маршрут по функции и параметру или по иаршруту и параметру
#        #return redirect(uri) #перенапрявляет по этому маршруту
#        #return HttpResponseRedirect(uri)#аналогично с использованием джанговского класса
#        #return HttpResponsePermanentRedirect('/')#аналогично с использованием джанговского класса
#        #raise Http404()  #если мы хотим поднять 404 ошибку при этом условии
#    return HttpResponse(f"<h1>Архив по годам</h1><p>{year}</p>")

def page_not_found(request, exception):
    return HttpResponseNotFound(f"<h1>Страница не найдена</h1>")

def addpage(request):
    return HttpResponse("Добавление статьи")

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

def show_category(request, cat_id):
    data = {
        'title': 'Отображение по рубрикам',
        'menu': menu,
        'posts': data_db,
        'cat_selected': cat_id,
    }

    return render(request, 'women/index.html', context=data)

