from tkinter import CASCADE
from django.db import models

class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to="pokemon_images", null=True)

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, null=True)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True)
    disappeared_at = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "PokemonEntities"
