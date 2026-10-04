from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    instructions = models.TextField() # Keeps whole raw workflow text string
    image_url = models.URLField(blank=True, max_length=500) # 👈 Add this field
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')

    def __str__(self):
        return self.title
