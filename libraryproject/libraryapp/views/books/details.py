import sqlite3
# from django.urls import reverse, redirect, reverse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from libraryapp.models import Book, Library, Librarian
from libraryapp.models import model_factory
from ..connection import Connection

# create_book(cursor, row):  A book is contained in a specific library and it was added to the inventory by a specific librarian. Those additional details must be retrieved by joining in the corresponding Library and Librarian entries via the foreign keys in each row. // ...update your get_book() function to include the appropriate JOIN clauses to get the details of the associated library and librarian. It also needs to use your new row factory function. (Nashville Software School, Chapter Documentation)
def create_book(cursor, row):
    _row = sqlite3.Row(cursor, row)

    book = Book()
    book.id = _row["book_id"]
    book.author = _row["author"]
    book.isbn_number = _row["isbn_number"]
    book.title = _row["title"]
    book.year_published = _row["year_published"]

    librarian = Librarian()
    librarian.id = _row["librarian_id"]
    librarian.first_name = _row["first_name"]
    librarian.last_name = _row["last_name"]

    library = Library()
    library.id = _row["library_id"]
    library.title = _row["library_name"]

    book.librarian = librarian
    book.location = library

    return book


# Also note that the book_id variable that you specified in the URLs pattern above gets automatically sent as an argument to the book_details view. (Nashville Software School, Chapter Documentation)
def get_book(book_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_book
        db_cursor = conn.cursor()

        
        db_cursor.execute("""
        SELECT
            b.id book_id,
            b.title,
            b.isbn_number,
            b.author,
            b.year_published,
            b.librarian_id,
            b.location_id,
            li.id librarian_id,
            u.first_name,
            u.last_name,
            loc.id library_id,
            loc.title library_name
        FROM libraryapp_book b
        JOIN libraryapp_librarian li ON b.librarian_id = li.id
        JOIN libraryapp_library loc ON b.location_id = loc.id
        JOIN auth_user u ON u.id = li.user_id
        WHERE b.id = ?
        """, (book_id,))

        return db_cursor.fetchone()

@login_required
def book_details(request, book_id):
    if request.method == 'GET':
        book = get_book(book_id)
        template = 'books/detail.html'
        context = {
            'book': book
        }
        
        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for editing a book
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE libraryapp_book
                SET title = ?,
                    author = ?,
                    isbn_number = ?,
                    year_published = ?,
                    location_id = ?
                WHERE id = ?
                """,
                (
                    form_data['title'], form_data['author'],
                    form_data['isbn_number'], form_data['year_published'],
                    form_data["location"], book_id,
                ))

            return redirect(reverse('libraryapp:books'))

        # Check if this POST is for deleting a book
        #
        # Note: You can use parenthesis to break up complex
        #       `if` statements for higher readability
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM libraryapp_book
                WHERE id = ?
                """, (book_id,))

            return redirect(reverse('libraryapp:books'))