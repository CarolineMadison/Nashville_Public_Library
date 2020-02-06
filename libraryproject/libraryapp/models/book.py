# Lightning Exercise: It's your job to create a Book model in the book.py module. A book should have the following properties.

# Title (CharField)
# ISBN number (CharField)
# Author (CharField)
# Year published (IntegerField)

# This import is needed for Python classes that are modeling a database table. (NSS, Chapter Documentation)
from django.db import models
from .library import Library
from .librarian import Librarian

class Book(models.Model):

    title = models.CharField(max_length=50)
    isbn_number = models.CharField(max_length=50) 
    author = models.CharField(max_length=50)
    year_published = models.IntegerField()
    location = models.ForeignKey(Library, on_delete=models.CASCADE)
    librarian = models.ForeignKey(Librarian, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("Book")
        verbose_name_plural = ("Books")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})
