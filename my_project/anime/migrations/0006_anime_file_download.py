# Generated by Django 5.1.1 on 2024-10-14 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0005_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='anime',
            name='file_download',
            field=models.FileField(blank=True, null=True, upload_to='series/', verbose_name='Файл для скачивания'),
        ),
    ]
