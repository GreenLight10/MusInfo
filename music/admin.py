from django.contrib import admin
from .models import *
from django.contrib.contenttypes.admin import GenericTabularInline

class MembersInline(admin.TabularInline):

    model = Artist.members.through

class ImageGalleryInline(GenericTabularInline):

    model = ImageGallery
    readonly_fields = ('image_url',)

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):

    inlines = [ImageGalleryInline]

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):

    inlines = [MembersInline, ImageGalleryInline]
    exclude = ('members',)


admin.site.register(Genre)
admin.site.register(Member)
admin.site.register(MediaType)
admin.site.register(ImageGallery)