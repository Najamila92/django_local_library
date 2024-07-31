from django.contrib import admin

from .models import Author, Book, Genre, BookInstance, Language

# Register your models here.

# admin.site.register(Author)
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # list view layout
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    # detail view layout
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    # Sectioning the detail view using fieldsets 



# admin.site.register(BookInstance)
@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'due_back', 'status')
    list_filter = ('status', 'due_back')

    # Sectioning the detail view using fieldsets 
    fieldsets = (
        (
            None, {'fields': ('id', 'book', 'imprint')} 
        ), 
        
        (
            'Availability', {'fields': ('status', 'due_back')}
        ),
    )

#inline BookInstance 
class BookInstanceInline(admin.TabularInline):
    model = BookInstance




# admin.site.register(Book)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'display_genre')
    inlines = [BookInstanceInline]


admin.site.register(Genre) 
admin.site.register(Language) 
