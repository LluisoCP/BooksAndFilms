from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from .forms import UploadBookForm, CommentBookForm

from django.http import HttpResponse

from .models import Book, Comment, Author # Film
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
    return render(request, 'project.html')

# MODEL LIST VIEWS
class BookListView(ListView):
    model = Book
    paginate_by = 6
    
#class FilmListView(ListView):
#	model = Film
#	paginate_by = 6

class AuthorListView(ListView):
    model = Author
    paginate_by = 6

# EDIT VIEWS
from django.contrib.auth.decorators import login_required

# @login_required(redirect_field_name='next', login_url=None)
@login_required
def UploadBookView(request):
	if request.method == 'POST':
		form = UploadBookForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('books')
	else:
		form = UploadBookForm()
	return render(request, 'items/upload_book.html', {
		'form': form
	})

from .forms import CreateAuthorForm
@login_required
def create_author(request):
	if request.method == 'POST':
		form = CreateAuthorForm(request.POST)
		if form.is_valid():
			form.save()
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
			new_comment.item = form.item = book
			new_comment.save()
			return redirect('book-details', pk=pk)
	else:
		form = CommentBookForm()
	comments = book.comments.all()
	context = {
		'book': book,
		'comments': comments,
		'form': form
	}
	return render(request, 'items/book_details.html', context = context)

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
