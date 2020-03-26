from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import generic
from .models import Book, Author, BookInstance, Genre, Language
from django.contrib import sessions
from django.contrib.auth.mixins import LoginRequiredMixin



class BookListView(generic.ListView):
    model = Book
    context_object_name = 'my_book_list'
    def get_queryset(self):
        return Book.objects.all()
    template_name = 'books/books.html'

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_detail_view(request, pk):
        try:
            book = Book.objects.get(pk=pk)
            context = {'book':book}
        except Book.DoesNotExist:
            raise Http404('Book does not exist')
        return render(request, template_name, context=context)

class AuthorListView(generic.ListView):
    model = Author
    context_object_name = 'author_list'

    def get_queryset(self):
        return Author.objects.all()
    template_name ='books/author_list.html'

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'books/author_detail.html'
    context_object_name = 'author'

    def get_author_detail_view(request, pk):
        try:
            author = Author.objects.get(pk=pk)
            context = {'author':author}
        except Author.DoesNotExist:
            raise Http404
        return render(request, template_namae, context=context)


class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name='loanedBooks/book_instance_list_borrowed_list.html'

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='0').order_by('due_back')
    
def index(request):
    num_book = Book.objects.all().count()
    num_instance = BookInstance.objects.all().count()

    # Availabel books status('a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    

    context = {
        'num_book':num_book,
        'num_instance':num_instance,
        'num_instances_available':num_instances_available,
        'num_authors':num_authors,
        'num_visits':num_visits,

    }

    return render(request, 'index.html', context=context)