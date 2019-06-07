from django.db import models
from django.urls import reverse
import datetime

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField('Born', null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    #This should be changed to 'author_details' para no marear
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
    
    class Meta:
        ordering: ['last_name']
        permissions = (("can_edit_author", "Edit author"),)
        

class Comment(models.Model):
    user = models.CharField(max_length=64)
    item = models.ForeignKey(
		'Book', #Posar Item? No
		related_name='comments',
		related_query_name='with_comments',
		on_delete=models.SET_NULL,
		null=True,
		blank=True #Millor False ? No
	)
	#Podria afegir-li un altre foreignKey vers Film i afegir als dos FK un default rollo 'This comment is for a book/film'. Llavors a cada form per crear un comment donar la possibilitat de indicar el tipus d'item que toca.
	# Llavors, per què anomenar-lo item? Dos fk, book i film
    content = models.CharField(max_length=1000)
    commented_at = models.DateTimeField(auto_now_add=True)
    GRADES = [(x,x) for x in range(0,11)]
    grade = models.SmallIntegerField(
        choices = GRADES,
		default=0,
		null=True
    )
        
        
class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=32, help_text='Enter a genre')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Item(models.Model):
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=400, null=True, blank=True)
    phrase = models.CharField(max_length=100, null=True, blank=True)
    
    YEAR_CHOICES = [(y,y) for y in range(1800, datetime.date.today().year+1)]
    release_year = models.SmallIntegerField(
		'Year',
        choices=YEAR_CHOICES,
        #blank=True,
		null=True,
        default=1800,
    )
    
    art = models.CharField(max_length=32, editable=False)
    
    LANG_CHOICES = (
        ('', 'Choose Languange'),
        ('EN', 'English'),
        ('FR', 'Français'),
        ('ES', 'Español'),
        ('CA', 'Català'),
        ('IT', 'Italiano'),
		('RU', 'Rusian'),
    )
    language = models.CharField(
		'Original Language',
        max_length=2,
        choices=LANG_CHOICES,
        blank=True,
        default='',
    )
    
    genres = models.ManyToManyField(
		Genre,
		help_text='Select a genre for this artpiece',
		related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
	)
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genres.all()[:3])
    display_genre.short_description ='Genre'
            
    def __str__(self):
        """String for representing the model object."""
        return self.title
    
    # ????
    class meta:
        abstract = True
        

def img_directory_path(instance, filename):
    return '{0}/{1}_{2}'.format(instance.art, instance.title, filename)
    # return 'books/{0}_{1}'.format(instance.title, filename)

class Book(Item):
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='uploads/books/', default='Books/books-default.jpg', null=True, blank=True)
    
    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/items/media/Books/books_default.jpg'
	
    # ???? up in the superclass
    class Meta:
        permissions = (("can_edit_book","Edit book"),)
        
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.art = 'Books'
        super(Book, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-details', args=[str(self.id)])
    
    # ???? up in the superclass
    def average_grade(self):
        """Returns the average grade of this item rounded to one decimal"""
        return round((sum(comment.grade for comment in self.comments.all()))/(self.comments.all().count()),1)
    
	
class Film(Item):
	director = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
	image = models.ImageField(upload_to='uploads/films/', default='uploads/films/films-default.jpg', null=True, blank=True)
    
	def save(self, *args, **kwargs):
		if not self.id:
			self.art = 'Films'
		super(Film, self).save(*args, **kwargs)
        
	def get_absolute_url(self):
		"""Returns the url to access a detail record for this book."""
		return reverse('film-detail', args=[str(self.id)])
    
    # ???? up in the superclass
	def average_grade(self):
		"""Returns the average grade of this item rounded to one decimal"""
		return round((sum(comment.grade for comment in self.comments.all()))/(self.comment.all().count()),1)