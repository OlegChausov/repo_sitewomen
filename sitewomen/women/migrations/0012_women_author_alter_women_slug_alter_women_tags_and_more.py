# Generated by Django 5.1.2 on 2024-12-15 13:07

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0011_women_photo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='women',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='women',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='women',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='tags', to='women.tagpost', verbose_name='Тэги'),
        ),
        migrations.AlterField(
            model_name='women',
            name='title',
            field=models.CharField(max_length=255, validators=[django.core.validators.MinLengthValidator(5, message='Минимум 5 символов'), django.core.validators.MaxLengthValidator(100, message='Максимум 100 символов')], verbose_name='Заголовок'),
        ),
    ]
