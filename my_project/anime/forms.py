from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import Anime, Comment, Profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите логин'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))


class RegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите логин',
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль',
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Повторите пароль',
    }))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя',
    }))

    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите фамилию',
    }))

    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите почту',
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class AddAnimeForm(forms.ModelForm):
    """Форма для добавления игры"""
    class Meta:
        model = Anime
        fields = ('title', 'description', 'image', 'video', 'release', 'category')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название аниме',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание',
            }),

            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),

            'video': forms.FileInput(attrs={
                'class': 'form-control',
            }),

            'release': forms.NumberInput(attrs={
                'class': 'form-control',
            }),

            'category': forms.SelectMultiple(attrs={
                'class': 'form-select',
            }),
        }


class CommentForm(forms.ModelForm):
    """Форма для комментариев"""
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст комментария'
            })
        }


class EditAccountForm(UserChangeForm):
    """Изменение аккаунта пользователя"""
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'old_password', 'new_password', 'confirm_password')

    username = forms.CharField(label='Никнейм', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    email = forms.EmailField(label='Почта', widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))

    old_password = forms.CharField(required=False, label='Старый пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    new_password = forms.CharField(required=False, label='Новый пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))

    confirm_password = forms.CharField(required=False, label='Подтвердите пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
    }))


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('city', 'about', 'avatar')

    city = forms.CharField(required=False, label='Город', widget=forms.TextInput(attrs={
        'class': 'form-class',
    }))

    about = forms.CharField(required=False, label='О себе', widget=forms.Textarea(attrs={
        'class': 'form-control',
    }))

    avatar = forms.FileField(required=False, label='Аватарка', widget=forms.FileInput(attrs={
        'class': 'form-control',
    }))
