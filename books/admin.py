from django.contrib import admin
from .models import Book, Comment, Rating

# Register your models here.

admin.site.register(Book)
admin.site.register(Comment)
admin.site.register(Rating)