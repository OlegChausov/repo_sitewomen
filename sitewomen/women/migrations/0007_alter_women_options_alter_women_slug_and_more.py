# Generated by Django 4.2.1 on 2024-10-16 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0006_alter_women_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='women',
            options={'ordering': ['-time_create']},
        ),
        migrations.AlterField(
            model_name='women',
            name='slug',
            field=models.SlugField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='women',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AddIndex(
            model_name='women',
            index=models.Index(fields=['-time_create'], name='women_women_time_cr_9f33c2_idx'),
        ),
    ]
