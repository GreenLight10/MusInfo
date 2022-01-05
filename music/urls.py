from django.urls import path

from . import views

app_name = 'music'
urlpatterns = [
    path('', views.IndexView.index, name='index'),
    path('about/', views.AboutView.about, name='about'),
]