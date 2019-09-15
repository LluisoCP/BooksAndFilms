from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/upload/', views.uploadBookView, name='upload-book'),
    path('books/<int:pk>', views.book_detail, name='book-details'),
    # path('films/', views.FilmListView.as_view(), name='films'),
    path('films/', views.filmListView, name='films'),
    path('films/<int:pk>', views.film_detail, name='film-detail'),
    path('films/add/', views.create_film, name='create-film'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.author_detail, name = 'author-detail'),
    path('genres/', views.genres, name='genres'),
    path('genres/<int:pk>', views.genre_items, name='genre_items'),
    path('genres/add/', views.createGenreView, name='add-genre'),
	path('the-project', views.project, name='project'),
]

# SEARCH FORM
urlpatterns += [
    path('search-form/', views.search_form, name='search_form'),
    path('search/', views.search, name='search'),
]

# CREATE AUTHOR
urlpatterns += [
    path('authors/add/', views.create_author, name = 'add-author')
]
#urlpatterns += [
#	path('signup/', views.signup, name='signup'),
#]

#To serve static images
#from django.conf import settings
#from django.conf.urls.static import static

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	
#if settings.DEBUG:
#	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	
	
from django.conf import settings
from django.urls import re_path
from django.views.static import serve

# ... the rest of your URLconf goes here ...

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
