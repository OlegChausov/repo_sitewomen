from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
import uuid

from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView

from .forms import AddPostForm, UploadFileForm
from .models import Women, Category, TagPost, UploadFiles
from .utils import DataMixin


# menu = [{'title': "О сайте", 'url_name': 'about'},
#         {'title': "Добавить статью", 'url_name': 'add_page'},
#         {'title': "Обратная связь", 'url_name': 'contact'},
#         {'title': "Войти", 'url_name': 'login'}
# ]


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

# class WomenHome(ListView): #без миксина
#     model = Women
#     template_name = 'women/index.html' #по умолчанию вызывается шаблон <имя приложения>/<имя модели>_list.html наш шаблон другой,  то его можно так переопределить
#     context_object_name = 'posts'  #по умолчанию в шаблон передается коллекция object_list (обычно квирисет из модели), но ее можно так переопределить, переназвать
#     extra_context = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'cat_selected': 0,
#     }#extra_context не умеет ловить данные динамически (GET)
#
#     def get_queryset(self):
#         return Women.published.all().select_related('cat') #переопределяем выборку (queryset) для переменной context_object_name/'posts'

class WomenHome(DataMixin, ListView): #с миксином
    template_name = 'women/index.html'
    context_object_name = 'posts'
    title_page = 'Главная страница'
    cat_selected = 0
    #на самом деле реализуем пагинацию в миксине, но можно и так:
    #paginate_by = 3 #классы ListView понимают пагинацию сразу. В шаблон передаются переменные page_obj - объект текущей страницы paginator - объект-пагинатор
    #потом через шаблон будет передаваться get запрос типа "?page=4" и пагинируемый context_object_name = 'posts' отобразит страницу

    def get_queryset(self):
        return Women.published.all().select_related('cat')




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

# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'cat_selected': 1,
#     }
#
#     return render(request, 'women/post.html', context=data)
#region ShowPost
# class ShowPost(DetailView): без миксина
#     #model = Women
#     template_name = 'women/post.html'
#     slug_url_kwarg = 'post_slug' #указываем переменную как в маршруте - post_slug
#     context_object_name = 'post'# по умолчанию в шаблон передается переменная object, но мы ее переназовем так, как указано в шаблоне
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = context['post']
#         context['menu'] = menu
#         return context
#
#     def get_object(self, queryset=None):# определяем, какой объект нам нельзя брать, а вместо него 404, тогда model = Women не пишем,
#         return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg]) #здесть передали не модель с фильтром, а МЕНЕДЖЕР, как объект
#endregion
class ShowPost(DataMixin, DetailView): #с миксином
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs),
                                      title='Главная страница',
                                      cat_selected=0)

    def get_object(self, queryset=None):
        return get_object_or_404(Women.published, slug=self.kwargs[self.slug_url_kwarg])

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


# def about(request): # без пагинации
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES) #создаем экземпляр формы
#         if form.is_valid():
#             fp = UploadFiles(file=form.cleaned_data['file']) #создаем экземпляр модели из экзеипляраформы
#             fp.save()
#     else:
#         form = UploadFileForm()
#
#     return render(request, 'women/about.html', {'title': 'О сайте', 'form': form})

@login_required(login_url='/admin/') #login_url='/admin/' также указывается в settings.py, но здесь выше приоритет
def about(request): #с пагинатором
    contact_list = Women.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'women/about.html', {'page_obj': page_obj, 'title': 'О сайте'})


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


# class AddPage(View):
#
#     def get(self, request):
#
#         form = AddPostForm()
#         data = {'title': 'Главная страница', 'menu': menu, 'form': form}
#         return render(request, 'women/addpage.html', data)
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#
#         data = {'title': 'Главная страница', 'menu': menu, 'form': form}
#
#         return render(request, 'women/addpage.html', data)
#
@permission_required(perm='women.view_women', raise_exception=True) #Здесь второй параметр raise_exception нужен для генерации кода 403 – доступ запрещен
def contact(request):
    return HttpResponse("Обратная связь")

def login(request):
    return HttpResponse("Авторизация")

# class AddPage(FormView):
#     form_class = AddPostForm #класс, как объект, без инициализации, ничего не создаем
#     template_name = 'women/addpage.html' #передаваяемая переменная в шаблон автоматом называется form
#     success_url = reverse_lazy('home') #лениво, почти асинхронно, определяет маршрут только при работе объекта класса AddPage(FormView)
#     extra_context = {
#         'menu': menu,
#         'title': 'Добавление статьи'}
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)

#без миксина
# class AddPage(CreateView): #     def form_valid(self, form): form.save() return super().form_valid(form) уже реализован в этом классе!
#     form_class = AddPostForm # можно так, а можнно и так:
#     #model = Women #альтернатива form_class = AddPostForm
#     #fields = '__all__' #альтернатива form_class = AddPostForm
#     #fields = ['title', 'slug', 'content', 'is_published', 'cat'] #альтернатива form_class = AddPostForm, только не __all__, а явно указанные, все обязательные поля должны быть!
#     template_name = 'women/addpage.html'
#     #success_url = reverse_lazy('home') можно не указывать, тогда выкинет на страницу def get_absolute_url(self): return reverse('post', kwargs={'post_slug': self.slug})
#     extra_context = {
#         'menu': menu,
#         'title': 'Добавление статьи'}

class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, CreateView):#с миксином
    model = Women
    fields = ['title', 'slug', 'content', 'is_published', 'cat']
    # form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home') #это первый приоритет, если указан. 2-й приеоритет - параметр next в шаблоне, это то, с чего попадаешь на форму авторизации, третий приоритет settings.py\LOGIN_URL = 'users:login'
    title_page = 'Добавление статьи'
    permission_required = 'women.add_women' #параметр для PermissionRequiredMixin. False/True берется из таблицы разрешений и редактируется в админке. синтаксис <приложение>.<действие>_<таблица>
    #login_url = '/admin/' #параметр для LoginRequiredMixin куда попадать если не пустило settings.py\LOGIN_URL = 'users:login', а потом сюда  login_url = '/admin/'

    def form_valid(self, form):
        w = form.save(commit=False) #сразу не сохраняем в БД
        w.author = self.request.user #в реквесте есть параметр, какой пользователь добавляет статью, тут то и сохраняем
        return super().form_valid(form)#тут-то и сохраняем

# class UpdatePage(UpdateView): #без миксина
#     model = Women
#     fields = ['title', 'content', 'photo', 'is_published', 'cat']
#     template_name = 'women/addpage.html'
#     success_url = reverse_lazy('home')
#     extra_context = {
#         'menu': menu,
#         'title': 'Редактирование статьи'}

class UpdatePage(PermissionRequiredMixin, DataMixin, UpdateView):#с миксином
    model = Women
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование статьи'
    permission_required = 'women.change_women'  # параметр для PermissionRequiredMixin. False/True берется из таблицы разрешений и редактируется в админке. синтаксис <приложение>.<действие>_<таблица>

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

# class WomenCategory(ListView): #без миксина
#     #model = Women в этом случае get_queryset не используем, а работаем с моделью целиком
#     template_name = 'women/index.html'
#     context_object_name = 'posts'
#     allow_empty = False #при пустом кверисете context_object_name = 'posts' --> (Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')) вернется 404
#     #extra_context = {еще переменные в модель}
#
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         cat = context['posts'][0].cat
#         context['title'] = 'Категория - ' + cat.name
#         context['menu'] = menu
#         context['cat_selected'] = cat.id
#         return context
#
#     def get_queryset(self):
#         return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat') #self.kwargs['cat_slug'] - это переменная, определенная в соответствующем маршруте women\urls.py

class WomenCategory(DataMixin, ListView):#с миксином
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Women.published.filter(cat__slug=self.kwargs['cat_slug']).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title='Категория - ' + cat.name,
                                      cat_selected=cat.pk,
                                      )

# def show_tag_postlist(request, tag_slug):
#     tag = get_object_or_404(TagPost, slug=tag_slug)#возвращает объект tag из модели TagPos по слагу если она есть, или 404
#     #posts = tag.tags.filter(is_published=Women.Status.PUBLISHED)# объект tag, через менеджер из методов объекта (related name) 'tags' ищем в модели posts нужные объекты post. Жадно загружаем все связанные с опубликованными постами данные из таблицы Category
#     posts = tag.tags.filter(is_published=Women.Status.PUBLISHED).select_related('cat')  # select_related('cat') это метод жадной загрузки объектов из модели women, связанное с модель 'Category' поле 'cat'
#     data = {
#         'title': f'Тег: {tag.tag}',
#         'menu': menu,
#         'posts': posts,
#         'cat_selected': None,
#     }
#
#     return render(request, 'women/index.html', context=data)

# class TagPostList(ListView): # без миксина
#     template_name = 'women/index.html'
#     context_object_name = 'posts'
#     allow_empty = False
#
#     def get_queryset(self):
#         return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')
#
#     # def get_context_data(self, *, object_list=None, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     cat = context['posts'][0].cat
#     #     context['title'] = 'Категория - ' + cat.name
#     #     context['menu'] = menu
#     #     context['cat_selected'] = cat.id
#     #     return context
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         my_tag = context['posts'][0].tags.filter(slug=self.kwargs['tag_slug'])[0]
#         context['title'] = 'Тег: ' + my_tag.tag
#         context['menu'] = menu
#         return context
#with mixin
class TagPostList(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Women.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')






