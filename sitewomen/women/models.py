from django.db import models
from django.urls import reverse

class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)

# Create your models here.
class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.DRAFT, verbose_name="Статус")# костыль, потому, нужно перевести  0 и 1 из class Status(models.IntegerChoices) в булевые значения
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name="Категории") #'posts' это алиас для women_set - вторичной модели
    #Класс 'Category' указан в виде строки т.к. в виде ссылки его еще может не существовать, н, вообще, если б был создан заранее, то можно передать через ссылку. PTOTECT -это ФУНКЦИЯ!
    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name="Тэги") #on_delete в этом классе отсутствует
    husband = models.OneToOneField('Husband', on_delete=models.SET_NULL, null=True, blank=True, related_name='wuman', verbose_name="Муж")#'wuman' - это алиса для обратногно связывания т.е. из связанного класса получить доступ связанным объектам Women


    objects = models.Manager() #старый дефолтный менеджер менеджер, существует без объявления класса
    published = PublishedModel() #новый менеджер


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'
        ordering=['-time_create']
        indexes=[models.Index(fields=['-time_create'])
        ]



    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug}) #маршрут 'category' + параметр slug из поля slug вызываемого объекта

    def __str__(self):
        return self.name


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    def __str__(self):
        return self.tag


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name