from django.contrib import admin
from .models import Recipe, Ingredient

# Register your models so they show up in the admin dashboard
admin.site.register(Recipe)
admin.site.register(Ingredient)