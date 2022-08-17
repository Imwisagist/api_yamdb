from django.contrib import admin

from .models import Category, Genre, Title, User

admin.site.register((Category, Genre, Title, User))
