from django.contrib import admin

from .models import Category, Genre, Title, User, Review, Comment

admin.site.register((Category, Genre, Title, User, Review, Comment))
