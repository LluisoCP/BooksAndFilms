from django.contrib import admin

from items.models import Book, Author, Genre, Comment
# Register your models here.
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Comment)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre', 'language')