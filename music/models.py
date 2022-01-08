import operator
from calendar import monthrange


from django.conf import settings

from django.db import models
from django.urls import reverse
from django.db import connection
from django.db.models.signals import post_save, pre_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

from django.utils.safestring import mark_safe

from utils import upload_function


class MediaType(models.Model):
    """Медианоситель"""
    name = models.CharField(max_length=100, verbose_name='Название медианосителя')
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Медианоситель'
        verbose_name_plural = 'Медианосители'


class Member(models.Model):
    """Музыкант"""
    name = models.CharField(max_length=255, verbose_name='Имя музыканта')
    slug = models.SlugField()
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Музыкант'
        verbose_name_plural = 'Музыканты'



class Genre(models.Model):
    """Музыкальный жанр"""
    name = models.CharField(max_length=50, verbose_name='Название жанра')
    slug = models.SlugField()
    description = models.TextField(verbose_name='Описание', default='Описание появится позже')
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('genre_detail', kwargs={'genre_slug': self.slug})
    
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Artist(models.Model):
    """Исполнитель"""
    name = models.CharField(max_length=255, verbose_name='Исполнитель/группа')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    members = models.ManyToManyField(Member, verbose_name='Участник', related_name='artist')
    image_gallery = GenericRelation('imagegallery')
    slug = models.SlugField()
    description = models.TextField(verbose_name='Описание', default='Описание появится позже')
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)
    def __str__(self):
        return f"{self.name} | {self.genre.name}"

    def get_absolute_url(self):
        return reverse('artist_detail', kwargs={'artist_slug': self.slug})
    
    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'

class Album(models.Model):
    """Альбом"""
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, verbose_name='Исполнитель')
    name = models.CharField(max_length=255, verbose_name='Название альбома')
    songs_list = models.TextField(verbose_name='Трэклист')
    release_date = models.DateField(verbose_name='Дата релиза')
    slug = models.SlugField()
    image = models.ImageField(upload_to=upload_function)


    def __str__(self):
        return f"{self.id} | {self.artist.name} | {self.name}"
    
    def get_absolute_url(self):
        return reverse('album_detail', kwargs={'artist_slug': self.artist.slug, 'album_slug': self.slug})

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'


class ImageGallery(models.Model):
    """Галерея изображений"""
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    image = models.ImageField(upload_to=upload_function)
    use_in_slider = models.BooleanField(default=False)

    def __str__(self):
        return f"Изображение для {self.content_object}"

    def image_url(self):
        return mark_safe(f'<img src="{self.image.url}" width="auto" height="200px"')

    class Meta:
        verbose_name = 'Галерея изображений'
        verbose_name_plural = verbose_name