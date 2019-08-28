from django.db import models
from django.urls import reverse
import datetime

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField('Born', null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    #GENRES = [('','Select the author\'s genre'),('M', 'Male'), ('F','Female'), ('X','Other')]
	#genre = models.CharField(max_length=1, choices=GENRES)
	#short_bio = models.CharField(max_length=255, blank=true, default='No biography has been set for this author')
	#ROLES = [('Writter', 'Writter'), ('Director', 'Director')]
	#role = models.CharField(max_length=8, choices=ROLES)
    #This should be changed to 'author_details' para no marear
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
    
    class Meta:
        ordering: ['last_name']
        

class Comment(models.Model):
    user = models.CharField(max_length=64)
    item = models.ForeignKey( #S'ha de dir book i repetir-lo per film
		'Book', #Posar Item? No (?)
		related_name='comments',
		related_query_name='with_comments',
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)
	#Podria afegir-li un altre foreignKey vers Film i afegir als dos FK un default rollo 'This comment is for a book/film'. Llavors a cada form per crear un comment donar la possibilitat de indicar el tipus d'item que toca.
	# Llavors, per què anomenar-lo item? Dos fk, book i film
    content = models.CharField(max_length=1000)
    commented_at = models.DateTimeField(auto_now_add=True)
    GRADES = [(x,x) for x in range(0,11)]
    grade = models.SmallIntegerField(
        choices = GRADES,
		default=0,
		null=True #False
    )
	#class Meta = [
	#	ordering = ['commented_at']
	#]
        
class Contact(models.Model):
    """Model to store the messages"""
    first_name = models.CharField(max_length=31)
    last_name = models.CharField(max_length=31)
    organisation = models.CharField(max_length=31)
    content = models.CharField(max_length=511)

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=32, help_text='Enter a genre')
    
    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Item(models.Model):
    """Abstract model serving as base model for Book and Film."""
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
	#Això podria ser un choice.
    
    LANG_CHOICES = (
        ('', 'Choose Languange'),
        ('EN', 'English'),
        ('FR', 'French'),
        ('ES', 'Spanish'),
        ('CA', 'Catalan'),
        ('IT', 'Italian'),
		('PT', 'Portuguese'),
		('GK', 'Greek'),
		('GM', 'German'),
		('AR', 'Arabic'),
		('RU', 'Rusian'),
		('JP', 'Japanese'),
		('CH', 'Chinese'),
		('TK', 'Turkish'),
		('DN', 'Danish'),
		('SW', 'Swedish'),
		('NW', 'Norwegian'),
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
    
    #def delete(self, *args, **kwargs #Try with file.delete
	#	if self.image:
	#	    name, storage = self.image.name, self.image.storage
    #        if storage.exists(name):
    #            storage.delete(name)
    #    super().delete(*args, **kwargs)  # Call the "real" save() method.
        
    # ????
    class meta:
        abstract = True
		#ordering = ['title']
        

def img_directory_path(instance, filename):
    return '{0}/{1}_{2}'.format(instance.art, instance.pk, instance.title)
    # return 'books/{0}_{1}'.format(instance.title, filename)

class Book(Item):
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='uploads/books/', default='Books/books-default.jpg', null=True, blank=True) #Això a la superclass
    
    def get_image(self): #i això
        if self.image:
            return self.image.url
        else:
            return '/items/media/{0}/default.jpg'.format(self.art) #Canvis !!
	
    # ???? up in the superclass
    #class Meta:
		#ordering = ['release_year'] per aplicar això cal override el valor de Item, és a dir iniciar així: class Meta(Item.Meta):
        
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.art = 'Book'
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
	image = models.ImageField(upload_to='uploads/films/', #Aquesta classe va a Item.
							  default='uploads/films/films-default.jpg', #Això no convé
							  null=True,
							  blank=True
	)
    
	def save(self, *args, **kwargs):
		if not self.id:
			self.art = 'Film'
		super(Film, self).save(*args, **kwargs)
        
	def get_absolute_url(self):
		"""Returns the url to access a detail record for this book."""
		return reverse('film-detail', args=[str(self.id)])
    
    # ???? up in the superclass
	def average_grade(self):
		"""Returns the average grade of this item rounded to one decimal"""
		return round((sum(comment.grade for comment in self.comments.all()))/(self.comment.all().count()),1)