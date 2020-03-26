from django.db import models
from django.urls import reverse
import uuid #For unique book instances as a reference
from django.contrib.auth.models import User
from datetime import date

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL,null=True)
    summary = models.TextField(max_length=1000, help_text='Brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField('Genre', help_text='Select the genre for this book')
    language = models.ManyToManyField('Language', help_text='Select the language of the book')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", kwargs={"pk": self.pk})

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[:3])
    display_genre.short_description ='Genre'
    


class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='A unique ID for this particular Book for the whole Library website')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintainance'),
        ('o', 'On Loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )
    
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book Availabilty'
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        # String for representing the book object
        return f'{self.id}({self.book.title})'

    def display_book(self):
        pass

 #Check if the book is overdue by comparing dates
 # 
    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        else:
            return false  

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def get_absolute_url(self):
        return reverse("author-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Genre(models.Model):
    name = models.CharField(max_length=120, help_text='Enter genre of the book here')

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=120, help_text='Enter the book language')

    def __str__(self):
        return self.name
    
    