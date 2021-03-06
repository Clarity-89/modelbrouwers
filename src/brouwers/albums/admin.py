from django.contrib import admin

from models import *


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'clean_title', 'last_upload', 'created', 'public', 'writable_to', 'order')
    list_editable = ('title', 'clean_title', 'public', 'order')
    list_filter = ('public', 'writable_to', 'created', 'trash')
    search_fields = ('=id', 'title', 'description')
    raw_id_fields = ('user', 'cover')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'name', 'order',)
    list_editable = ('name', 'order',)
    search_fields = ('name',)


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'album', 'views', 'uploaded')
    list_filter = ('album', 'uploaded')
    raw_id_fields = ('user', 'album')


class PreferencesAdmin(admin.ModelAdmin):
    list_display = ('user', 'auto_start_uploading')
    list_editable = ('auto_start_uploading',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user',)


class AlbumDownloadAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'album', 'downloader', 'timestamp', 'failed')
    list_filter = ('timestamp', 'failed')
    search_fields = ('album__title', 'downloader__username')
    raw_id_fields = ('downloader', 'album')


class AlbumGroupAdmin(admin.ModelAdmin):
    list_display = ('__unicode__',)
    search_fields = ('album__title',)
    filter_horizontal = ('users',)

admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Preferences, PreferencesAdmin)
admin.site.register(AlbumDownload, AlbumDownloadAdmin)
admin.site.register(AlbumGroup, AlbumGroupAdmin)
