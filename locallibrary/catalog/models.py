from django.db import models
from django.urls import reverse # used in get_absolute_url() to get URL for specified ID 
from django.db.models import UniqueConstraint   # constrains fields to unique values
from django.db.models.functions import Lower    # Returns lower cased value of field 

import uuid # Required for unique book instances

#GENRE MODEL
class Genre(models.Model):
    """ Model representing a book genre. """
    name = models.CharField(max_length=200, unique=True, help_text="Enter a book genre (e.g. Science Fiction, French Poetry, etc.)")


    def __str__(self):
        """ String for representing the model object. """
        return self.name 

    def get_absolute_url(self):
        """ Returns the url to access a particular genre instance. """ 
        return reverse('genre-details', args=[str(self.id)])
    
    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'), 
                name = 'genre_name_case_insensitive_unique', 
                violation_error_message = "Genre already exists (case insensitive match)"
            ),
        ]


# BOOK MODEL
class Book(models.Model):
    """ Model representing a book (but not a specific copy of a book). """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    # Foreign key used because book can only have multiple books. 
    # Author as a string rather than object because it hasn't been declared yet in the file 
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn"> ISBN Number </a>')

    # ManyToManyField used because genre can contain many books. Books can cover many genres. 
    # Genre class has already been defined so we can specify the object above 

    genre = models.ManyToManyField(Genre, help_text="Select a genre for this book") 
    language = models.ForeignKey('Language', on_delete=models.RESTRICT, help_text="Select a Language the book was written in")

    def __str__(self):
        """ String for representing the Model object. """
        return self.title
    
    def get_absolute_url(self):
        """ Return the absolute url to access a detail record for this book. """
        return reverse('book-details', args=[str(self.id)])
    
    def display_genre(self):
        """ this will display the genre which is a many to may field. """
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    
    display_genre.short_description = 'Genre'

# BOOKINSTANCE MODEL    
class BookInstance(models.Model):
    """ Model representing a specific copy of a book (i.e that can be borrowed from the library). """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On Loan'), 
        ('a', 'Available'), 
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text="book availability")
    

    class Meta: 
        ordering = ['due_back']

    
    def __str__(self):
        """ String for representing the model object. """
        return f'{self.id} ({self.book.title})'
    

# AUTHOR MODEL 
class Author(models.Model):
    """ Model representing an author """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta: 
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self): 
        """ Return the URL to access a particular author instance. """
        return reverse('author-details', args=[str(self.id)])
    
    def __str__(self):
        """ String for representing the model object. """
        return f'{self.last_name}, {self.first_name}' 

# LANGUAGE MODEL 
class Language(models.Model):
    """ A Model Representing a Language. """
    name = models.CharField(max_length=100, unique=True, help_text="Enter a New Language")

    class Meta: 
        ordering = ['name']

        constraints = [
            UniqueConstraint(
                Lower('name'), 
                name = 'language_name_case_insensitive_unique', 
                violation_error_message = "Language already exists (case insensitive match)"
            ),
        ]

    def get_absolute_url(self): 
        """ Return the URL to access a particular author instance. """
        return reverse('language-details', args=[str(self.id)]) 
    
    def __str__(self):
        """ String for representing the model object. """
        return self.name 