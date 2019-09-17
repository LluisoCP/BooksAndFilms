from django.db import models
from django.urls import reverse
import datetime
        
class Contact(models.Model):
    """Model to store the messages"""
    first_name = models.CharField(max_length=31)
    last_name = models.CharField(max_length=31)
    organisation = models.CharField(max_length=31)
    content = models.CharField(max_length=511)

class Author(models.Model):
    """Model representing an author."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField('Born', null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    GENRES = [('','Select the author\'s genre'),('M', 'Male'), ('F','Female'), ('X','Other')]
    genre = models.CharField(max_length=1, choices=GENRES)
    short_bio = models.CharField(max_length=255, blank=True, default='No biography has been set for this author')
    ROLES = [('Writter', 'Writter'), ('Director', 'Director')]
    role = models.CharField(max_length=8, choices=ROLES)

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'
    
    def full_name(self):
        """Returns the author's full name"""
        return f'{self.last_name}, {self.first_name}'

    class Meta:
        ordering: ['last_name']
        

class Comment(models.Model):
    user = models.CharField(max_length=64)
    book = models.ForeignKey(
		'Book',
		related_name='comments',
		related_query_name='whose_comments',
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)
    film = models.ForeignKey(
        'Film',
        related_name='comments',
        related_query_name='whose_comments',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    content = models.CharField(max_length=1000)
    commented_at = models.DateTimeField(auto_now_add=True)
    GRADES = [(x,x) for x in range(0,11)]
    grade = models.SmallIntegerField(
        choices = GRADES,
		default=5,
    )
    class Meta:
    	ordering = ['-commented_at']

class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=32, help_text='Enter a genre', unique=True)
    def get_absolute_url(self):
        """Returns url to access the detail page of the genre"""
        return reverse('genre_items', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_num_genre(self):
        """Returns the number of artpieces of the genre"""
        # return self.items_related.count() #canviar si canvio name_related
        return self.books_related.count() #canviar si canvio name_related

class Item(models.Model):
    """Abstract model serving as base model for Book and Film."""
    created_at = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=32, unique=True)
    description = models.CharField(max_length=400, blank=True)
    phrase = models.CharField(max_length=100, blank=True)
    
    YEAR_CHOICES = [(y,y) for y in range(1800, datetime.date.today().year+1)]
    release_year = models.SmallIntegerField(
		'Year',
        choices=YEAR_CHOICES,
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
    )
    
    genres = models.ManyToManyField(
		Genre,
		help_text='Select the genres for this artpiece',
		related_name="%(class)ss_related",#items_related
        related_query_name="whose_%(class)ss",#whose_items
	)
    def display_genre(self):
        """Create a string for the Genre. This is required to display genre in Admin."""
        return ', '.join(genre.name for genre in self.genres.all()[:3])
    display_genre.short_description ='Genre'
            
    def __str__(self):
        """String for representing the model object."""
        return self.title
    
#    def get_image(self):
#        if self.image:
#            return self.image.url
#        else:
#            return '/items/static/{0}s-default.jpg'.format(self.art) #Ho deixo aquí o ho baixo?

#    def delete(self, *args, **kwargs):
#		if self.image:
#		    name, storage = self.image.name, self.image.storage
#            if storage.exists(name):
#                storage.delete(name)
#        super().delete(*args, **kwargs)
        
    class Meta:
        abstract = True
        ordering = ['title']
        
def b_img_directory_path(instance, filename):
    return 'books/{0}_{1}'.format(instance.pk, instance.title)
    #return '{0}/{1}_{2}'.format(instance.art, instance.pk, instance.title)

class Book(Item):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=b_img_directory_path,null=True, blank=True)

    def get_image(self): #i això
        if self.image:
            return self.image.url
        else:
            return '/items/static/{0}s-default.jpg'.format(self.art) #Canvis !!

    def delete(self, *args, **kwargs):
        if self.image:
            name, storage = self.image.name, self.image.storage
            if storage.exists(name):
                storage.delete(name)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.id:
            self.art = 'book'
        super(Book, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-details', args=[str(self.id)])
    
    # ???? up in the superclass
    def average_grade(self):
        """Returns the average grade of this item rounded to one decimal"""
        return round((sum(comment.grade for comment in self.comments.all()))/(self.comments.all().count()),1)
    
def f_img_directory_path(instance):
    return 'films/{0}_{1}'.format(instance.pk, instance.title)
    #return '{0}/{1}_{2}'.format(instance.art, instance.pk, instance.title)

class Film(Item):
    director = models.ForeignKey(Author, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=f_img_directory_path, null=True, blank=True)
    
    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return '/items/static/{0}s-default.jpg'.format(self.art)

    def delete(self, *args, **kwargs):
        if self.image:
            name, storage = self.image.name, self.image.storage
            if storage.exists(name):
                storage.delete(name)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.id:
            self.art = 'film'
        super(Film, self).save(*args, **kwargs)
        
    def get_absolute_url(self):
        """Returns the url to access a detail record for this book"""
        return reverse('film-detail', args=[str(self.id)])
    
    def average_grade(self):
        """Returns the average grade of this item rounded to one decimal"""
        return round((sum(comment.grade for comment in self.comments.all()))/(self.comment.all().count()),1)