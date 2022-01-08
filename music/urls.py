from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    BaseView, 
    ArtistDetailView, 
    AlbumDetailView,
    GenreDetailView, 
    RegistrationView, 
    LoginView, 
    SearchView,
    ArtistsView,
    GenresView)


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('search/', SearchView.as_view(), name='search'),
    path('artists/', ArtistsView.as_view(), name='artists'),
    path('genres/', GenresView.as_view(), name='genres'),
    path('<str:artist_slug>/', ArtistDetailView.as_view(), name='artist_detail'),
    path('genres/<str:genre_slug>/', GenreDetailView.as_view(), name='genre_detail'),
    path('<str:artist_slug>/<str:album_slug>/', AlbumDetailView.as_view(), name='album_detail')
]