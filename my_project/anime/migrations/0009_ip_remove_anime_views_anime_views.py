# Generated by Django 5.1.1 on 2024-10-15 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anime', '0008_alter_profile_about_alter_profile_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=20, verbose_name='IP пользователя')),
            ],
            options={
                'verbose_name': 'ip пользователя',
                'verbose_name_plural': 'ip пользователей',
            },
        ),
        migrations.RemoveField(
            model_name='anime',
            name='views',
        ),
        migrations.AddField(
            model_name='anime',
            name='views',
            field=models.ManyToManyField(blank=True, null=True, related_name='anime_views', to='anime.ip', verbose_name='Количество просмотров'),
        ),
    ]
