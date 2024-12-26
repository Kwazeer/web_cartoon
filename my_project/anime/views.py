from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.http import FileResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.db.models import Q

from .models import Category, Anime, Comment, Profile, Ip
from .forms import LoginForm, RegistrationForm, AddAnimeForm, CommentForm, EditAccountForm, EditProfileForm
from .tests import get_user_ip
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class AnimeListView(ListView):
    """Все категории главной страницы"""
    model = Anime
    context_object_name = 'animes'
    template_name = 'anime/index.html'
    extra_context = {
        'title': 'Бесплатное аниме'
    }


class AnimeCategoryList(AnimeListView):
    """Аниме по категориям на главной странице"""
    def get_queryset(self):
        anime = Anime.objects.filter(category__id=self.kwargs['pk'])
        return anime

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(id=self.kwargs['pk'])
        context['title'] = f'Качай {category.title}'
        return context


class AnimeDetailView(DetailView):
    """Страница с деталями аниме"""
    model = Anime
    context_object_name = 'anime'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        anime = Anime.objects.get(pk=self.kwargs['pk'])
        # Список рекомендаций без повторений и фильтрация по всем категориям, которые есть у аниме
        recommended_anime = Anime.objects.filter(
            Q(category__in=anime.category.all()) & ~Q(pk=self.kwargs['pk'])).distinct()

        context['title'] = anime.title
        context['comments'] = Comment.objects.filter(anime=anime)
        context['recommended_anime'] = recommended_anime
        ip = get_user_ip(self.request)  # Проверка на IP адрес для просмотров
        if Ip.objects.filter(ip=ip).exists():
            anime.views.add(Ip.objects.get(ip=ip))
        else:
            Ip.objects.create(ip=ip)
            anime.views.add(Ip.objects.get(ip=ip))
        if self.request.user.is_authenticated:  # Проверка на авторизацию для оставления комментариев
            context['comment_form'] = CommentForm()
        return context


def user_login_view(request):
    """Страница для авторизации пользователя"""
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {user.username}')
                return redirect('index')
            else:
                messages.error(request, 'Вы ввели неверный логин или пароль')
                return redirect('login')
        else:
            messages.error(request, 'Вы ввели неверный логин или пароль')
            return redirect('login')

    else:
        form = LoginForm()

    context = {
        'title': 'Страница авторизации',
        'login_form': form,
    }

    if not request.user.is_authenticated:
        return render(request, 'anime/login.html', context)
    else:
        return redirect('index')


def user_logout_view(request):
    """Выход из аккаунта"""
    logout(request)
    messages.warning(request, 'Вы вышли из своего аккаунта')
    return redirect('index')


def user_register_view(request):
    """Страница регистрации пользователя"""
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)  # Сохраняет пользователя в профиль
            profile.save()
            messages.success(request, 'Регистрация прошла успешно.\nПожалуйста, авторизуйтесь!')
            return redirect('login')
        else:
            for field in form.errors:
                # Поле для отображения конкретной ошибки во время регистрации
                messages.error(request, form.errors[field].as_text())
                return redirect('registration')

    else:
        form = RegistrationForm()

    context = {
        'title': 'Страница регистрации',
        'register_form': form,
    }

    if not request.user.is_authenticated:
        return render(request, 'anime/registration.html', context)
    else:
        return redirect('index')


class AnimeAddView(CreateView):
    """Добавление нового аниме"""
    form_class = AddAnimeForm
    model = Anime
    template_name = 'anime/add_anime.html'

    def get(self, request, *args, **kwargs):
        """Защита"""
        if not self.request.user.is_staff:
            return redirect('index')
        else:
            # Если получилось, то отработай этот класс (добавление нового аниме)
            super(AnimeAddView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = 'Добавление аниме'
        context['add_form'] = self.get_form()
        return context


class AnimeUpdateView(UpdateView):
    """Изменение аниме"""
    form_class = AddAnimeForm
    model = Anime
    template_name = 'anime/add_anime.html'

    def get(self, request, *args, **kwargs):
        """Защита"""
        if not self.request.user.is_staff:
            return redirect('index')
        else:
            # Если получилось, то отработай этот класс (добавление нового аниме)
            return super(AnimeUpdateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        anime = Anime.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'Изменение - {anime.title}'
        context['add_form'] = self.get_form()
        return context


class AnimeDeleteView(DeleteView):
    """Удаление аниме"""
    model = Anime
    context_object_name = 'anime'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        """Защита"""
        if not self.request.user.is_staff:
            return redirect('index')
        else:
            # Если получилось, то отработай этот класс (добавление нового аниме)
            return super(AnimeDeleteView, self).get(request, *args, **kwargs)


class AnimeSearchView(AnimeListView):
    """Осуществление поиска игр"""
    def get_queryset(self):
        word = self.request.GET.get('q')
        anime = Anime.objects.filter(title__iregex=word)
        return anime


def save_comment_view(request, pk):
    """Сохранение комментария"""
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.anime = Anime.objects.get(pk=pk)
        comment.save()

        return redirect('anime_detail', pk)


class CommentUpdateView(UpdateView):
    """Изменение комментария"""
    model = Comment
    form_class = CommentForm
    template_name = 'anime/anime_detail.html'

    def get(self, request, *args, **kwargs):
        user = request.user if request.user.is_authenticated else None
        comment = Comment.objects.get(pk=self.kwargs['pk'], user=user)
        if not comment.user == user:
            return redirect('index')
        else:
            return super(CommentUpdateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        anime = Anime.objects.get(pk=comment.anime.pk)
        comments = Comment.objects.filter(anime=anime)
        comments = [i for i in comments if i.pk != comment.pk]  # Скрытие изменяемого комментария
        context['title'] = anime.title
        context['anime'] = anime
        context['comments'] = comments
        context['comment_form'] = self.get_form()
        return context

    def get_success_url(self):
        return reverse('anime_detail', kwargs={'pk': self.object.anime.pk})


def comment_delete_view(request, comment_pk, anime_pk):
    """Удаление комментария"""
    user = request.user if request.user.is_authenticated else None
    comment = Comment.objects.get(user=user, pk=comment_pk, anime=anime_pk)
    if comment.user == user:
        comment.delete()

    return redirect('anime_detail', anime_pk)


def download_serial(request, pk):
    """Скачивание аниме"""
    if request.user.is_authenticated:
        anime = Anime.objects.get(pk=pk)
        response = FileResponse(open(anime.file_download.path, mode='rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment; filename=%s' % anime.file_download.name

        return response

    else:
        anime = Anime.objects.get(pk=pk)
        #  Ограничение на скачивание файла только для пользователей
        messages.error(request, 'Только авторизованные пользователи могут скачивать файлы')
        return redirect('anime_detail', anime.pk)


def profile_view(request, username):
    """Страница с профилем пользователя"""
    user = request.user if request.user.is_authenticated else None
    if user:
        profile = Profile.objects.get(user=user)
        comments = Comment.objects.filter(user=user)
        count_comments = len(comments)

        context = {
            'title': f'Профиль {user}',
            'profile': profile,
            'comments': comments,
            'count': count_comments,
        }

        return render(request, 'anime/profile.html', context)

    else:
        messages.error(request, 'Авторизуйтесь, чтобы перейти в профиль')
        return redirect('login')


def edit_profile_account_view(request, username):
    """Страница для редактирования профиля и аккаунта"""
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        profile = Profile.objects.get(user=request.user)
        if profile:
            context = {
                'title': f'Изменение данных {request.user.username}',
                'edit_profile_form': EditProfileForm(instance=request.user.profile),
                'edit_account_form': EditAccountForm(instance=request.user),
            }

            return render(request, 'anime/edit_profile.html', context)
        else:
            return redirect('login')


def edit_account_view(request):
    """Форма для изменения аккаунта"""
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            account_form = EditAccountForm(request.POST, instance=request.user)
            if account_form.is_valid():
                account_form.save()
                data = account_form.cleaned_data
                user = User.objects.get(id=request.user.id)

                if user.check_password(data['old_password']):
                    if data['old_password'] and data['new_password'] == data['confirm_password']:
                        user.set_password(data['new_password'])
                        user.save()
                        update_session_auth_hash(request, user)
                        messages.success(request, 'Данные успешно изменены')

                        return redirect('profile', user.username)
                    else:
                        for field in account_form.errors:
                            messages.error(request, account_form.errors[field].as_text())
                            return redirect('edit', user.username)
                else:
                    for field in account_form.errors:
                        messages.error(request, account_form.errors[field].as_text())
                        return redirect('edit', user.username)

                return redirect('profile', user.username)

            else:
                for field in account_form.errors:
                    messages.error(request, account_form.errors[field].as_text())
                    return redirect('edit', request.user.username)


def edit_profile_view(request):
    """Форма для изменения профиля"""
    if not request.user.is_authenticated:
        return redirect('login')

    else:
        if request.method == 'POST':
            profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile', request.user.username)

            else:
                for field in profile_form.errors:
                    messages.error(request, profile_form.errors[field].as_text())
                    return redirect('edit', request.user.username)
