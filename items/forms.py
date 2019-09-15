from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import Book, Comment, Author, Genre, Contact, Film

class ContactForm(forms.ModelForm):
    class Meta:
    	model = Contact
    	fields = ['first_name', 'last_name', 'organisation', 'content',]
    	widgets = {
            'content': forms.Textarea
        }

class UploadBookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ['title', 'author', 'genres', 'release_year', 'language', 'description', 'image']
		widgets = {
            'description': forms.Textarea,
            'genres': forms.CheckboxSelectMultiple
        }
		

class CommentBookForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['user', 'content', 'grade']
		widgets = {
            'content': forms.Textarea
        }

class CreateFilmForm(forms.ModelForm):
    
    class Meta:
    	model = Film
    	fields = ['title', 'director', 'genres', 'release_year', 'description', 'image']
    	widgets = {
    		'description': forms.Textarea,
    		'genres': forms.CheckboxSelectMultiple
    	}
	
class CreateAuthorForm(forms.ModelForm):
	class Meta:
		model = Author
		fields =['first_name', 'last_name', 'date_of_birth', 'date_of_death',] #Afegir role i genre
		
# REGISTRATION / AUTHENTICATION

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#BUILT-IN
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=32, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=64, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required.')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', ]
		
# Should I try CreateView ?? Didn't work
class CreateGenreForm(forms.ModelForm):
    class Meta:
        model = Genre
        fields = ['name',]

# CUSTOM
class CreateUserForm(forms.Form):
	username = forms.CharField(max_length=32)
	first_name = forms.CharField(required=False)
	last_name = forms.CharField(required=False)
	password1=forms.CharField(max_length=32,widget=forms.PasswordInput()) #render_value=False
	password2=forms.CharField(max_length=32,widget=forms.PasswordInput())
	email=forms.EmailField(required=False)

	def clean_username(self): # check if username exists
		try:
			User.objects.get(username=self.cleaned_data['username']) #get user from user model
		except User.DoesNotExist:
			return self.cleaned_data['username']

		raise forms.ValidationError("Your username already exists")


	def clean(self): # check if password 1 and password2 match each other
		if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:#check if both pass first validation
			if self.cleaned_data['password1'] != self.cleaned_data['password2']: # check if they match each other
				raise forms.ValidationError("The passwords you've input dont match.")

		return self.cleaned_data


	def save(self): # create new user
		new_user=User.objects.create_user(self.cleaned_data['username'],
									  self.cleaned_data['email'],
									  self.cleaned_data['password1'])
		new_user.first_name = self.cleaned_data['first_name']
		new_user.last_name = self.cleaned_data['last_name']
		new_user.save()
		return new_user