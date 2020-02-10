import sqlite3
# from django.urls import reverse, redirect, reverse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from libraryapp.models import Book, Library
from libraryapp.models import model_factory
from ..connection import Connection

# Also note that the book_id variable that you specified in the URLs pattern above gets automatically sent as an argument to the book_details view. (Nashville Software School, Chapter Documentation)
def get_librarian(librarian_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Book)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            l.id,
            l.location_id,
            l.user_id,
            a.first_name,
            a.last_name,
            a.email,
            a.username
        FROM libraryapp_librarian l
        JOIN auth_user a on l.user_id = a.id
        WHERE l.id = ?
        """, (librarian_id,))

        return db_cursor.fetchone()

@login_required
def librarian_details(request, librarian_id):
    if request.method == 'GET':
        librarian = get_librarian(librarian_id)

        template = 'librarians/detail.html'
        context = {
            'librarian': librarian
        }
        
        return render(request, template, context)