# Generated by Django 4.2.1 on 2024-10-13 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='women',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255, verbose_name='URL'),
        ),
        migrations.AlterField(
            model_name='women',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Заголовок'),
        ),
    ]
