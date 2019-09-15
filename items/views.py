from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView # Unneeded

from .forms import UploadBookForm, CommentBookForm, CreateGenreForm, ContactForm, CreateFilmForm

from django.http import HttpResponse

from .models import Book, Comment, Author, Genre, Film
from django.db.models import Q


# MAIN VIEW
def index(request):
    """View function for the main page if the site"""
    num_books = Book.objects.all().count()
    img_books = Book.objects.exclude(pk=2).exclude(pk=7) # Eliminar
    num_img_books = img_books.count()
    img_data = range(num_img_books)
	#img_books = Book.objects.exclude(Q(pk=2) | Q(pk=7))
    context = {
        'num_books': num_books,
        'img_books': img_books,
		'img_data': img_data
    }
    return render(request, 'index.html', context=context)

# THE PROJECT VIEW
def project(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)
		if form.is_valid():
			form.save()
			request.session['has_commented'] = True
			return redirect('project')
	else:
		form = ContactForm()
		has_commented = request.session.get('has_commented', False)
		request.session['has_commented'] = False
		return render(request, 'project.html', {'form': form, 'has_commented': has_commented})

# MODEL LIST VIEWS
def genres(request):
    genres = Genre.objects.all()
    has_commented = request.session.get('has_commented', False)
    request.session['has_commented'] = False
    return render(request, 'items/genres.html', {'genres': genres, 'has_commented': has_commented})

def genre_items(request, pk):
    genre = get_object_or_404(Genre, pk=pk)
    books = Book.objects.filter(genres__name=genre.name)
    #films = Film.objects.filter(genres__name=genre.name)
    context = {
    	'genre': genre,
    	'books': books,
    	#'films': films,
    }
    return render(request, 'items/genre_items.html', context=context)

class BookListView(ListView):
    model = Book
    paginate_by = 6
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Store the session has_commented value (default False)
        has_commented = self.request.session.get('has_commented', False)
        # Add the stored value to the context
        context['has_commented'] = has_commented
        # Once the session is stored, reset it to False
        self.request.session['has_commented'] = False
        return context
    
# Per provar això hi ha que migrar
def filmListView(request):
    return render(request, 'items/film_list.html', {'film_list': False})

#class FilmListView(ListView):
#	model = Film
#	paginate_by = 6
#	def get_context_data(self, **kwargs):
#		context = super().get_context_data(**kwargs)
#		has_commented = self.request.session.get('has_commented', False)
#		context['has_commented'] = has_commented
#		self.request.session['has_commented'] = False
#		return context


class AuthorListView(ListView):
    model = Author
    paginate_by = 6
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Get the session has_commented value
        has_commented = self.request.session.get('has_commented', False)
        self.request.session['has_commented'] = False
        # Add in the new context parameter
        context['has_commented'] = has_commented
        return context

# EDIT VIEWS
from django.contrib.auth.decorators import login_required

@login_required
def createGenreView(request):
    if request.method == 'POST':
    	form = CreateGenreForm(request.POST)
    	if form.is_valid():
    		form.save()
    		request.session['has_commented'] = True
    		return redirect('genres')
    else:
    	form = CreateGenreForm()
    return render(request, 'items/genre_form.html', {'form': form})


# @login_required(redirect_field_name='next', login_url=None)
@login_required
def uploadBookView(request):
	if request.method == 'POST':
		form = UploadBookForm(request.POST, request.FILES)
		if form.is_valid():
			# form.save()
			newBook = form.save()
			request.session['has_commented'] = True
			# return redirect('books')
			return redirect('book-details', pk=newBook.id)
	else:
		form = UploadBookForm()
	return render(request, 'items/upload_book.html', {
		'form': form
	})

@login_required
def create_film(request):
    if request.method == 'POST':
    	form = CreateFilmForm(request.POST, request.FILES)
    	if form.is_valid():
    		form.save()
    		request.session['has_commented'] = True
    		return redirect('films')
    else:
    	form = CreateFilmForm()
    return render(request, 'items/film_create.html', {'form': form})

from .forms import CreateAuthorForm
@login_required
def create_author(request):
	if request.method == 'POST':
		form = CreateAuthorForm(request.POST)
		if form.is_valid():
			form.save()
			request.session['has_commented'] = True
			return redirect('authors')
	else:
		form = CreateAuthorForm()
	return render(request, 'items/author_create.html', {
		'form': form
	})

# DETAIL VIEWS
from django.shortcuts import get_object_or_404

def book_detail(request, pk):
	book = get_object_or_404(Book, pk=pk) #Prova això
	if request.method == 'POST':
		form = CommentBookForm(request.POST)
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.item = form.item = book #Canviar item per book
			new_comment.save()
			request.session['has_commented'] = True
			return redirect('book-details', pk=pk)
	else:
		form = CommentBookForm(initial={'user':request.user.first_name+' '+request.user.last_name}) if request.user.is_authenticated else CommentBookForm()

	comments = book.comments.all()
	has_commented = request.session.get('has_commented', False)
	request.session['has_commented'] = False
	context = {
		'book': book,
		'comments': comments,
		'form': form,
		'has_commented': has_commented
	}
	return render(request, 'items/book_details.html', context = context)

def film_detail(request, pk):
	film = get_object_or_404(Film, pk=pk) #Prova això
	if request.method == 'POST':
		# A canviar
		form = CommentBookForm(request.POST) # Does it make sense to have two different comment forms?
		if form.is_valid():
			new_comment = form.save(commit=False)
			new_comment.item = form.item = film # Is form.item needed here? Change item=>film
			new_comment.save()
			request.session['has_commented'] = True
			return redirect('film-detail', pk=pk)
	else:
		form = CommentBookForm() #A canviar

	comments = film.comments.all()
	has_commented = request.session.get('has_commented', False)
	request.session['has_commented'] = False
	context = {
		'film': film,
		'comments': comments,
		'form': form,
		'has_commented': has_commented
	}
	return render(request, 'items/film_detail.html', context = context)

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.filter(author__pk=pk)
	#if author.role == 'Director':
    	#films = Film.objects.filter(author__pk=pk)
    context = {
        'author': author,
        'books': books
		#'items': 'items'
    }
    return render(request, 'items/artist_detail.html', context)

# SEARCH VIEWS
def search_form(request):
    return render(request, 'items/search_form.html')

from django.db.models import Q
def search(request):
    if 'search-input' in request.GET and request.GET['search-input']:
        entry_terms = request.GET['search-input']
        term_list = entry_terms.split(' ', 3)
        if (len(term_list)>3): #Eliminar tots els termes més ennlà del tercer.
	        term_list = term_list[0:3]
        first_term = term_list.pop(0)
        book_qs = Book.objects.filter(title__icontains=first_term)
        author_qs = Author.objects.filter(Q(first_name__icontains=first_term) | Q(last_name__icontains=first_term))
        return_terms = [first_term]
        while (term_list):
            book_qs2 = Book.objects.filter(title__icontains=term_list[0])
            book_qs = book_qs.union(book_qs2)
            author_qs2 = Author.objects.filter(Q(first_name__icontains=term_list[0]) | Q(last_name__icontains=term_list[0]))
            author_qs = author_qs.union(author_qs2)
            return_terms = return_terms + [term_list.pop(0)]
        context = {
            'books': book_qs,
            'authors': author_qs,
            'terms': return_terms,
        }
        return render(request, 'items/search_results.html', context=context)
    else:
        message = 'You submitted an empty form.'
        return render(request, 'items/search_form.html', context = {'message': message})
	
# REGISTRATION / AUTHENTICATION

from django.contrib.auth import login, authenticate

# CUSTOM SIGNUP VIEW
from .forms import SignUpForm #, CreateUserForm

def signup(request):
	next='/'
	if request.GET:
		next = request.GET['next']

	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect(next)
	else:
		form = SignUpForm()
	return render(request, 'signup.html', {'form': form})

# CUSTOM LOGIN VIEW

#def login_user(request):
#    username = password = ''
#    next = ""

#    if request.GET:  
#        next = request.GET['next']

#    if request.POST:
#        username = request.POST['username']
#        password = request.POST['password']

#        user = authenticate(username=username, password=password)
#        if user is not None:
#			login(request, user)
#			if !next:
#				return HttpResponseRedirect('/')
#			else:
#				return HttpResponseRedirect(next)
#		else:
#			errmsg = 'Your credentials didn\'t match any member'
#			return render(request, 'login_user.html',{'username': username, 'next':next, 'errmsg': errmsg})
			
#    return render(request, 'login_user.html',{'username': username, 'next':next})
