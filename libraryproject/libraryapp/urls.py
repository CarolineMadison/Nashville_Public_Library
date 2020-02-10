# This file defines all of the URLs that libraryapp will respond to.
from .views import *
from django.urls import include, path
# from django.urls import path

app_name = "libraryapp"

urlpatterns = [
    path('', home, name='home'),
    path('books/', book_list, name='books'),
    path('librarians/', librarian_list, name='librarians'),
    path('libraries/', library_list, name="libraries"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', logout_user, name='logout'),
    path('books/form', book_form, name='book_form'),
    path('libraries/form', library_form, name='library_form'),
    path('books/<int:book_id>/', book_details, name='book'),
]