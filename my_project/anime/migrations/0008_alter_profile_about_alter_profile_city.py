# Generated by Django 5.1.1 on 2024-10-14 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0007_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='about',
            field=models.CharField(default='Не указано', max_length=200, verbose_name='О себе'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(default='Не указано', max_length=50, verbose_name='Город'),
        ),
    ]
