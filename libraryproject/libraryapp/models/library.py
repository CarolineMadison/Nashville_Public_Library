# This import is needed for Python classes that are modeling a database table. (NSS, Chapter Documentation)
from django.db import models

class Library(models.Model):

    title = models.CharField(max_length=50)
    address = models.CharField(max_length=100)

    class Meta:
        verbose_name = ("Library")
        verbose_name_plural = ("Librarys")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("Library_detail", kwargs={"pk": self.pk})
