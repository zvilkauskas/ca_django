from django.shortcuts import render, get_object_or_404
from .models import Genre, Book, BookInstance, Author
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
# su class
from django.contrib.auth.mixins import LoginRequiredMixin
# su def
from django.contrib.auth.decorators import login_required
# Registration imports
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

# Forms imports
from django.shortcuts import render, reverse, get_object_or_404
from .forms import BookReviewForm
# Importuojame FormMixin, kurį naudosime BookDetailView klasėje
from django.views.generic.edit import FormMixin

#user profile pics imports
from django.contrib.auth.decorators import login_required

# form edit imports
from .forms import BookReviewForm, UserUpdateForm, ProfileUpdateForm

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

# arba saugesnis variantas:

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


class BookDetailView(FormMixin, generic.DetailView):
    model = Book
    template_name = 'book_detail.html'
    form_class = BookReviewForm

    # nurodome, kur atsidursime komentaro sėkmės atveju.
    def get_success_url(self):
        return reverse('book-detail', kwargs={'pk': self.object.book_id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(BookDetailView, self).form_valid(form)




# paieška
def search(request):
    """
    paprasta paieška.
    query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    # query ima informaciją iš paieškos laukelio
    query = request.GET.get('query')
    # search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    # Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės didžiosios/mažosios.
    # title ir description Dpavadinimai ateina iš models.py Book klasės. Galima sudėti net ir visus.
    search_results = Book.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query) | Q(author__first_name__icontains=query))
    return render(request, 'search.html', {'books': search_results, 'query': query})


# ________________USER BOOK VIEWS________________

# galimi du variantai su class ir def
# variantas su class
class UserBooksListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'user_books.html'
    paginate_by = 2

    def get_queryset(self):
        return BookInstance.objects.filter(reader=self.request.user, book_status__exact='t').order_by('due_back')


#variantas su def
@login_required(login_url='login')
def user_books(request):
    user = request.user
    try:
        user_books = BookInstance.objects.filter(reader=request.user).filter(book_status__exact='t').order_by('due_back')
    except BookInstance.DoesNotExist:
        user_books = None

    context = {
        'user': user,
        'user_books': user_books,
    }
    return render(request, 'user_books2.html', context)

# Registration function
@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')


# Sutrumpintas destytojo variantas
#     if password != password2:
#         messages.error(request, 'Slaptažodžiai nesutampa!')
#         return redirect('register')
#
#     if User.objects.filter(username=username).exists():
#         messages.error(request, f'Vartotojo vardas {username} užimtas!')
#         return redirect('register')
#
#     if User.objects.filter(email=email).exists():
#         messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
#         return redirect('register')
#
#     User.objects.create_user(username=username, email=email, password=password)
#     messages.info(request, f'Vartotojas {username} užregistruotas!')
#     return redirect('login')

# user profile
@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)



