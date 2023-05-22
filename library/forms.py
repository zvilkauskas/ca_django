from .models import BookReview, Profile, Author, BookInstance, Book
from django import forms
# formu redagavimo importai
from django.contrib.auth.models import User


class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ('content', 'book', 'reviewer',)
        widgets = {'book': forms.HiddenInput(), 'reviewer': forms.HiddenInput()}


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['photo']

#   PVZ SU FORMOM
# class AddAuthorForm(forms.ModelForm):
#     class Meta:
#         model = Author
#         fields = ['fist_name', 'last_name'] #arba '__all__' jei norim visus elementus is klases paimti
#
#         widgets = {'first_name': forms.CheckboxInput(attrs={'checked': True})}
#
#         error_messages = {
#             NON_FIELD_ERRORS: {
#                 'unique_together': 'Sitas autorius jau turi tokia knyga!'
#             }
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(AddAuthorForm, self).__init__(*args, **kwargs)
#         self.fields['first_name'].required = True
#         self.field['book_status'].choices = [('', 'Select book status...')]+ BookInstance.LOAN_STATUS

# class AddNewBook(forms.ModelForm):
#     class Meta:
#         model = Book
#         fields = ['author', 'title', 'description', 'isbn', 'genre', 'cover'] #arba '__all__' jei norim visus elementus is klases paimti
#
#         widgets = {'title': forms.TextInput(attrs={'placeholder': 'Enter book title...'})}
#
#     # Django form overriding
#     def __init__(self, *args, **kwargs):
#         super(AddNewBook, self).__init__(*args, **kwargs)
#         self.fields['first_name'].required = True
#         self.field['author'].queryset = Author.objects.order_by('first_name')
#         self.field['cover'].required = False

class CreateBookInstanceForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'due_back']


class EditBookInstanceForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['book', 'due_back', 'book_status']

        widgets = {
            'book': forms.HiddenInput,
        }