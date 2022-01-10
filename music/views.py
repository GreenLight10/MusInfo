from django.core import paginator
from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django import forms, views
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.views.generic import ListView
from django.core.paginator import Paginator

from .models import *
from .forms import LoginForm, RegistrationForm, SearchForm
# Create your views here.

class BaseView(views.View):
    def get(self, request, *args, **kwargs):
        import random
        genres = random.sample(list(Genre.objects.all()), 4)
        artists = random.sample(list(Artist.objects.all()), 4)
        context = {
            'genres': genres,
            'artists': artists,
        }

        return render(request, 'base.html', context)

class ArtistsView(ListView):
    def get(self, request, *args, **kwargs):
        artists = Artist.objects.all().order_by('name')
        paginator = Paginator(artists, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'artists': artists,
            'page_obj': page_obj,
        }

        return render(request, 'artists.html', context)

class GenresView(ListView):
    def get(self, request, *args, **kwargs):
        genres = Genre.objects.all().order_by('name')
        paginator = Paginator(genres, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'genres': genres,
            'page_obj': page_obj,
        }

        return render(request, 'genres.html', context)

class NewsView(views.View):
    def get(self, request, *args, **kwargs):
        news = News.objects.all().order_by('-date')
        context = {
            'news': news,
        }

        return render(request, 'news.html', context)


class NewDetailView(views.generic.DetailView):

    model = News
    template_name = 'new/new_detail.html'
    slug_url_kwarg = 'new_slug'
    context_object_name = 'new'


class ArtistDetailView(views.generic.DetailView):

    model = Artist
    template_name = 'artist/artist_detail.html'
    slug_url_kwarg = 'artist_slug'
    context_object_name = 'artist'
    # def get(self, request, *args, **kwargs):
    #     artists = Artist.objects.all().order_by('-id')[:5]
    #     context = {
    #         'artists': artists,
    #     }
    #     return render(request, 'artist/artist_detail.html', context)


class AlbumDetailView(views.generic.DetailView):

    model = Album
    template_name = 'album/album_detail.html'
    slug_url_kwarg = 'album_slug'
    context_object_name = 'album'

class GenreDetailView(views.generic.DetailView):

    model = Genre
    template_name = 'genre/genre_detail.html'
    slug_url_kwarg = 'genre_slug'
    context_object_name = 'genre'



class LoginView(views.View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'login.html', context)
    
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user =authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'login.html', context)


class RegistrationView(views.View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'registration.html', context)


class SearchView(views.View):

    def get(self, request, *args, **kwargs):
        form = SearchForm(request.GET)
        results = None
        if form.is_valid():
            q = Q()
            artist = form.cleaned_data['artist']
            if artist:
                q.add(Q(**{'artist': artist}), Q.AND)
            genre = form.cleaned_data['genre']
            if genre:
                if len(genre) == 1:
                    q.add(Q(**{'artist__genre__slug': genre[0]}), Q.AND)
                else:
                    q.add(Q(**{'artist__genre__slug__in': genre}), Q.AND)
            release_date_from = form.cleaned_data['release_date_from']
            if release_date_from:
                q.add(Q(**{'release_date__gte': release_date_from}), Q.AND)
            release_date_to = form.cleaned_data['release_date_to']
            if release_date_to:
                q.add(Q(**{'release_date__lte': release_date_to}), Q.AND)
            
            if q:
                results = Album.objects.filter(q)
            else:
                results = Album.objects.none()
                
        context = {
            'form': form
        }

        if results and results.exists():
            context.update({'results': results})
            
        return render(request, 'search.html', context)
        