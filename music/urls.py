from django.urls import path
from django.contrib.auth.views import LogoutView
from django.views.decorators.cache import cache_page

from .views import *


urlpatterns = [
    path('', cache_page(60)(BaseView.as_view()), name='base'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('search/', SearchView.as_view(), name='search'),
    path('artists/', cache_page(60)(ArtistsView.as_view()), name='artists'),
    path('genres/', cache_page(60)(GenresView.as_view()), name='genres'),
    path('news/', NewsView.as_view(), name='news'),
    path('<str:artist_slug>/', ArtistDetailView.as_view(), name='artist_detail'),
    path('genres/<str:genre_slug>/', GenreDetailView.as_view(), name='genre_detail'),
    path('news/<str:new_slug>/', NewDetailView.as_view(), name='new_detail'),
    path('<str:artist_slug>/<str:album_slug>/', AlbumDetailView.as_view(), name='album_detail')
]