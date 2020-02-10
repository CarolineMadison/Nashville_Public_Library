import sqlite3
from django.shortcuts import render, redirect, reverse
from libraryapp.models import Library
from libraryapp.models import Book
from ..connection import Connection
from libraryapp.models import model_factory
from django.contrib.auth.decorators import login_required

def create_library(cursor, row):
    _row = sqlite3.Row(cursor, row)

    library = Library()
    library.id = _row["id"]
    library.title = _row["title"]
    library.address = _row["address"]

    # Note: You are adding a blank books list to the library object
    # This list will be populated later (see below)
    library.books = []

    book = Book()
    book.id = _row["book_id"]
    book.title = _row["book_title"]
    book.author = _row["author"]
    book.isbn_number = _row["isbn_number"]
    book.year_published = _row["year_published"]

    # Return a tuple containing the library and the
    # book built from the data in the current row of
    # the data set
    return (library, book,)

@login_required
def library_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            
            conn.row_factory = create_library
            db_cursor = conn.cursor()

            db_cursor.execute("""
                SELECT
                    li.id,
                    li.title,
                    li.address,
                    b.id book_id,
                    b.title book_title,
                    b.author,
                    b.year_published,
                    b.isbn_number
                FROM libraryapp_library li
                JOIN libraryapp_book b ON li.id = b.location_id
            """)

            # When you instruct the sqlite3 package to fetchall(), it takes your SQL string and walks over to the database and executes it. It then takes all of the rows that the database generates, and creates a tuple out of each one. It then puts all of those tuples into a list. (Chapter Documentation, NSS)

            # TUPLE is a collection which is ordered and unchangeable. Allows duplicate members. Parenthesis. (W3 Schools)

            # LIST is a collection which is ordered and changeable. Allows duplicate members. Brackets. (W3 Schools)

            all_libraries = db_cursor.fetchall()

            # code commented out because model_factor(Library) does this
            # for row in dataset:
            #     # creating an instance of a library with Library()
            #     library = Library()
            #     library.id = row['id']
            #     library.title = row['title']
            #     library.address = row['address']

            #     all_libraries.append(library)

        # When a view wants to generate some HTML representations of data, it needs to specify a template to use. [Below], the template variable is holding the path and filename of the template. (Nashville Software School, Ch 3 Documentation)
            # Start with an empty dictionary
            library_groups = {}

        # Iterate the list of tuples
        for (library, book) in all_libraries:

    # If the dictionary does have a key of the current
    # library's `id` value, add the key and set the value
    # to the current library
            if library.id not in library_groups:
                library_groups[library.id] = library
                library_groups[library.id].books.append(book)

    # If the key does exist, just append the current
    # book to the list of books for the current library
            else:
                library_groups[library.id].books.append(book)
                template = 'libraries/list.html'

        # the dictionary 'all_libraries' has a single property labeled all_libraries and its value is the list of library objects that the view generates. // The key name is able to be used in a loop in the template.  (Nashville Software School, Ch 3 Documentation)
        template = 'libraries/list.html'

        context = {
            'all_libraries': library_groups.values()
        }
        # Then the render() method is invoked. That method takes the HTTP request as the first argument, the template to be used as the second argument, and then a dictionary containing the data to be used in the template. (Nashville Software School, Ch 3 Documentation)
        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO libraryapp_library
            (
                title, address
            )
            VALUES (?, ?)
            """,
            (form_data['title'], form_data['address']))

        return redirect(reverse('libraryapp:libraries'))
    