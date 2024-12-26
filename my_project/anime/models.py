from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.contrib import admin


class Category(models.Model):
    """Модель категорий"""
    title = models.CharField(max_length=50, verbose_name='Название категории')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('anime_category', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'категорию'
        verbose_name_plural = 'категории'


class Anime(models.Model):
    """Модель аниме"""
    title = models.CharField(max_length=100, verbose_name='Название аниме')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='image/', blank=True, null=True, verbose_name='Изображение')
    video = models.FileField(upload_to='video/', blank=True, verbose_name='Видео')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    views = models.ManyToManyField('Ip', related_name='anime_views', null=True, blank=True,
                                   verbose_name='Количество просмотров')
    category = models.ManyToManyField(Category, verbose_name='Категория')
    release = models.IntegerField(blank=True, null=True, verbose_name='Дата создания')
    file_download = models.FileField(upload_to='series/', blank=True, null=True, verbose_name='Файл для скачивания')

    def __str__(self):
        return self.title

    @admin.display(description='Просмотры')  # Декоратор на изменение имени в админке (from django.contrib import admin)
    def count_views(self):
        """Подсчёт комментариев"""
        if self.views:
            return self.views.count()
        else:
            return 0

    def get_absolute_url(self):
        return reverse('anime_detail', kwargs={'pk': self.pk})

    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/media/image/test.png'

    def get_video(self):
        if self.video:
            return self.video.url
        else:
            return ''

    def display_categories(self):
        """Вывод списка категорий в админ панель"""
        return ', '.join([value.title for value in self.category.all()])

    # Verbose_name, но без класса Meta
    display_categories.short_description = 'Категории'

    class Meta:
        verbose_name = 'аниме'
        verbose_name_plural = 'аниме'


class Comment(models.Model):
    """Модель комментариев"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Пользователь')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, verbose_name='Аниме')
    text = models.CharField(max_length=200, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        """Проверка для избежания ошибки"""
        if self.user:
            return self.user.username
        return 'Удалённый аккаунт'

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'


class Profile(models.Model):
    """Модель профиля пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    avatar = models.FileField(upload_to='avatar/', blank=True, null=True, verbose_name='Аватарка')
    about = models.CharField(max_length=200, default='Не указано', verbose_name='О себе')
    city = models.CharField(max_length=50, default='Не указано', verbose_name='Город')
    allow_comments = models.BooleanField(default=True, verbose_name='Право на публикацию')

    def __str__(self):
        return self.user.username

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            return '/media/avatar/test_avatar.png'

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'


class Ip(models.Model):
    """Модель для сохранения IP адресов"""
    ip = models.CharField(max_length=20, verbose_name='IP пользователя')

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = 'ip пользователя'
        verbose_name_plural = 'ip пользователей'
