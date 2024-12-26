from django.urls import path
from .views import *

urlpatterns = [
    path('', AnimeListView.as_view(), name='index'),
    path('category/<int:pk>/', AnimeCategoryList.as_view(), name='anime_category'),
    path('anime/<int:pk>/', AnimeDetailView.as_view(), name='anime_detail'),
    path('login/', user_login_view, name='login'),
    path('logout/', user_logout_view, name='logout'),
    path('registration/', user_register_view, name='registration'),
    path('add_anime/', AnimeAddView.as_view(), name='add_anime'),
    path('anime/<int:pk>/update/', AnimeUpdateView.as_view(), name='update_anime'),
    path('anime/<int:pk>/delete/', AnimeDeleteView.as_view(), name='delete_anime'),
    path('search/', AnimeSearchView.as_view(), name='search_anime'),
    path('save_comment/<int:pk>/', save_comment_view, name='save_comment'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='update_comment'),
    path('comment/<int:comment_pk>/<int:anime_pk>/delete/', comment_delete_view, name='delete_comment'),
    path('download/<int:pk>/', download_serial, name='download_anime'),
    path('profile/<str:username>/', profile_view, name='profile'),
    path('profile_change/<str:username>/', edit_profile_account_view, name='edit'),
    path('edit_account/', edit_account_view, name='edit_account'),
    path('edit_profile/', edit_profile_view, name='edit_profile'),
]
