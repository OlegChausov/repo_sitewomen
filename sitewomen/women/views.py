from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
import uuid

from django.views import View
from django.views.generic import TemplateView, ListView

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
]


# def index(request):
#     # posts = Women.objects.filter(is_published=1) это со старым дефолтным менеджером
#     #posts = Women.published.all()# all вместо filter потому, что этот менеджер возвращает только те записи, которые нужны, фильтровать не нужно
#     posts = Women.published.all().select_related('cat') #select_related('cat') это метод жадной загрузки объектов из модели women, связанное с модель 'Category' поле 'cat'
#
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': posts,
#        # 'cat_selected': 0,  # не обязательная строчка
#     }
#     return render(request, 'women/index.html', context=data)
#     #return HttpResponse(render_to_string('women/index.html')) альтернативный вариаент

class WomenHome(ListView):
    model = Women
    template_name = 'women/index.html' #по умолчанию вызывается шаблон <имя приложения>/<имя модели>_list.html наш шаблон другой,  то его можно так переопределить
    context_object_name = 'posts'  #по умолчанию в шаблон передается коллекция object_list (обычно квирисет из модели), но ее можно так переопределить, переназвать
    extra_context = {
        'title': 'Главная страница',
        'menu': menu,
        'cat_selected': 0,
    }#extra_context не умеет ловить данные динамически (GET)

    def get_queryset(self):
        return Women.published.all().select_related('cat') #переопределяем выборку (queryset) для переменной context_object_name/'posts'

# class WomenHome(TemplateView):
#     template_name = 'women/index.html'
#     # вариант логики, чтобы передать в шаблон простые данные, не подходит, чтобы ловить динамически получениые (GET) данные
#     extra_context = {
#          'title': 'Главная страница',
#          'menu': menu,
#          'posts': Women.published.all().select_related('cat'),
#          'cat_selected': 0,
#      }
#
#     # def get_context_data(self, **kwargs): # вариант логики, чтобы передать в шаблон в том числе динамически получениые (GET) данные
#     #     context = super().get_context_data(**kwargs) #берем словарь базового класса, и дабавляем в него свои данные
#     #     context['title'] = 'Главная страница'
#     #     context['menu'] = menu
#     #     context['posts'] = Women.published.all().select_related('cat')
#     #     context['cat_selected'] = int(self.request.GET.get('cat_id', 0)) #добавляем динамически данные, которые мы ловим на лету из get запроса
#     #     return context

def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'cat_selected': 1,
    }

    return render(request, 'women/post.html', context=data)


def handle_uploaded_file(f):
    name = f.name
    ext = ''

    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]

    suffix = str(uuid.uuid4())
    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# def about(request): #тут делаем загрузку просто в каталог, не связанною с моделью БД
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(form.cleaned_data['file'])# "file" это из формы UploadFileForm атрибут-алиас такой label="Файл"
#     else:
#         form = UploadFileForm()
#
#     return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})

def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES) #создаем экземпляр формы
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file']) #создаем экземпляр модели из экзеипляраформы
            fp.save()
    else:
        form = UploadFileForm()

    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu, 'form': form})

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


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # try: #такая вот проверка валидности
#             #     Women.objects.create(**form.cleaned_data)# звездочки распаковывают словарь form.cleaned_data - атрибут объекта form в виде словаря
#             #     return redirect('home')
#             # except:
#             #     form.add_error(None, 'Ошибка добавления поста')
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#
#     return render(request, 'women/addpage.html', {'menu': menu, 'title': 'Добавление статьи', 'form': form})


class AddPage(View):

    def get(self, request):

        form = AddPostForm()
        data = {'title': 'Главная страница', 'menu': menu, 'form': form}
        return render(request, 'women/addpage.html', data)

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

        data = {'title': 'Главная страница', 'menu': menu, 'form': form}

        return render(request, 'women/addpage.html', data)

def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")


# def show_category(request, cat_slug):
#     category = get_object_or_404(Category, slug=cat_slug) #ищем по модели Category, поле slug, 404 поднимается, если не найдено. Потом ту строчку (объект), что нашли возрващаем в posts = Women.published.filter(cat_id=category.pk) с атрибутом pk
#     #posts = Women.published.filter(cat_id=category.pk)
#     posts = Women.published.filter(cat_id=category.pk).select_related('cat') #select_related('cat') это метод жадной загрузки объектов из модели women, связанное с модель 'Category' поле 'cat'
#     data = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': category.pk,
#     }
#
#     return render(request, 'women/index.html', context=data)

class WomenCategory(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False #при пустом кверисете context_object_name = 'posts' --> (Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')) вернется 404

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context['title'] = 'Категория - ' + cat.name
        context['menu'] = menu
        context['cat_selected'] = cat.id
        return context

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat') #self.kwargs['cat_slug'] - это переменная, определенная в соответствующем маршруте women\urls.py


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

