from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from .models import Women, Category, TagPost

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


def index(request):
    # posts = Women.objects.filter(is_published=1) это со старым дефолтным менеджером
    #posts = Women.published.all()# all вместо filter потому, что этот менеджер возвращает только те записи, которые нужны, фильтровать не нужно
    posts = Women.published.all().select_related('cat') #select_related('cat') это метод жадной загрузки объектов из модели women, связанное с модель 'Category' поле 'cat'

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


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug) #ищем по модели Category, поле slug, 404 поднимается, если не найдено. Потом ту строчку (объект), что нашли возрващаем в posts = Women.published.filter(cat_id=category.pk) с атрибутом pk
    #posts = Women.published.filter(cat_id=category.pk)
    posts = Women.published.filter(cat_id=category.pk).select_related('cat') #select_related('cat') это метод жадной загрузки объектов из модели women, связанное с модель 'Category' поле 'cat'
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }

    return render(request, 'women/index.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)#возвращает объект tag из модели TagPos по слагу если она есть, или 404
    #posts = tag.tags.filter(is_published=Women.Status.PUBLISHED)# объект tag, через менеджер из методов объекта (related name) 'tags' ищем в модели posts нужные объекты post. Жадно загружаем все связанные с опубликованными постами данные из таблицы Category
    posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')  # select_related('cat') это метод жадной загрузки объектов из модели women, связанное с модель 'Category' поле 'cat'
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }

    return render(request, 'women/index.html', context=data)

