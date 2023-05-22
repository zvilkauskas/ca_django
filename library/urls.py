from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('authors/', views.authors, name='authors'),
    path('authors/<int:author_id>', views.author, name='author'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('search/', views.search, name='search'),
    path('account/', include('django.contrib.auth.urls')),
    # Views for user taken books and book
    #su class
    path('my_books/', views.UserBooksListView.as_view(), name='my-books'),
    #su def
    path('my_books2/', views.user_books, name='my-books2'),
    #su class
    path('my_books/<uuid:pk>', views.UserBookDetailView.as_view(), name='my-book'),
    # su def
    path('my_books2/<uuid:book_instance_id>', views.user_book, name='my-book2'),
    # CreateView su class
    path('my_books/create', views.UserBookCreateView.as_view(), name='create'),
    # UpdateView su class
    path('my_books/update/<uuid:pk>', views.UserBookUpdateView.as_view(), name='update'),
    # DeleteView su class
    path('my_books/delete/<uuid:pk>', views.UserBookDeleteView.as_view(), name='delete'),
    # CreateView su def
    path('my_books/create2', views.create_new_book_instance, name='create2'),
    # UpdateView su def
    path('my_books/update2/<uuid:pk>', views.update_book_instance, name='update2'),
    #Login and profile
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]