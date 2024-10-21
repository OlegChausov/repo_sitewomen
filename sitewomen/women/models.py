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
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='posts') #'posts' это алиас для women_set - вторичной модели
    #Класс 'Category' указан в виде строки т.к. в виде ссылки его еще может не существовать, н, вообще, если б был создан заранее, то можно передать через ссылку. PTOTECT -это ФУНКЦИЯ!

    objects = models.Manager() #старый дефолтный менеджер менеджер, существует без объявления класса
    published = PublishedModel() #новый менеджер


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug}) #маршрут 'category' + параметр slug из поля slug вызываемого объекта

    def __str__(self):
        return self.name