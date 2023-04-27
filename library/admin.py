from django.contrib import admin

# Register your models here.

from .models import *


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'display_books')


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description', 'display_genre')
    # paieška case sensitive
    search_fields = ('title',)


class BookInstanceAdmin(admin.ModelAdmin):
    #datos pakeitimas iš amerikietiškos į europinę stulpelio pavadinime
    def available_on(self, obj):
        return obj.due_back.strftime('%Y-%m-%d')

    list_display = ('book', 'book_status', 'available_on')
    # jeigu vienas elementas tuplo viduje, butinai reikia gale , pvz: ('book_status',)
    list_filter = ('book_status', 'due_back')
    fieldsets = (
        ('General', {'fields': ('instance_id', 'book')}),
        ('Availability', {'fields': ('book_status', 'due_back')}),
    )
    search_fields = ('instance_id', 'book__title')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookInstance, BookInstanceAdmin)
admin.site.register(Genre)
