from django.db import models
from django.urls import reverse

class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published="1")

# Create your models here.
class Women(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=1)#choices=Status.choices, default=Status.DRAFT)

    objects = models.Manager()
    published = PublishedModel()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})