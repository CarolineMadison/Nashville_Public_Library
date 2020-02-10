import sqlite3
from django.shortcuts import render, redirect, reverse
from libraryapp.models import Library
from ..connection import Connection
from libraryapp.models import model_factory
from django.contrib.auth.decorators import login_required

@login_required
def library_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            
            conn.row_factory = model_factory(Library)
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

        template = 'libraries/list.html'

        # the dictionary 'all_libraries' has a single property labeled all_libraries and its value is the list of library objects that the view generates. // The key name is able to be used in a loop in the template.  (Nashville Software School, Ch 3 Documentation)

        context = {
            'all_libraries': all_libraries
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
    