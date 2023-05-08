from django.shortcuts import render, get_object_or_404
from .models import Genre, Book, BookInstance, Author
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q


def index(request):
    book_count = Book.objects.all().count()
    book_instance_count = BookInstance.objects.all().count()
    available_books_count = BookInstance.objects.filter(book_status__exact='a').count()

    author_count = Author.objects.all().count()

    number_of_visits = request.session.get('number_of_visits', 1)
    request.session['number_of_visits'] = number_of_visits + 1

    context = {
        'books': book_count,
        'book_instances': book_instance_count,
        'authors': author_count,
        'available': available_books_count,
        'number_of_visits': number_of_visits
    }

    return render(request, "index.html", context)

def authors(request):
    paginator = Paginator(Author.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_authors = paginator.get_page(page_number)
    context = {
        'authors': paged_authors
    }
    return render(request, 'authors.html', context=context)

# Autoriaus aprašymas
# def author(request, author_id):
#     author = Author.objects.get(author_id)
#     context = {
#         'author': author
#     }
#     return render(request, 'author.html', context)

#arba saugesnis variantas:

def author(request, author_id):
    single_author = get_object_or_404(Author, pk=author_id)
    return render(request, 'author.html', {'author': single_author})

class BookListView(generic.ListView):
    model = Book
    paginate_by = 2
    template_name = 'book_list.html'

    # #papildomai info po sarasu
    # def get_context_data(self, **kwargs):
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     context['duomenys'] = 'eilutė iš lempos'
    #     return context

class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'book_detail.html'


# paieška
def search(request):
    """
    paprasta paieška.
    query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    #query ima informaciją iš paieškos laukelio
    query = request.GET.get('query')
    #search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    #Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės didžiosios/mažosios.
    #title ir description Dpavadinimai ateina iš models.py Book klasės. Galima sudėti net ir visus.
    search_results = Book.objects.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(author__first_name__icontains=query))
    return render(request, 'search.html', {'books': search_results, 'query': query})
