from email.base64mime import header_length
from email.policy import default
from tkinter import CASCADE
from django.db import models

class Pokemon(models.Model):
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="pokemon_images", default=None, blank=True)

    def __str__(self):
        return self.title

class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(null=True, blank=True)
    disappeared_at = models.DateTimeField(null=True, blank=True)
    level = models.IntegerField(null=True, default=None, blank=True)
    health = models.IntegerField(null=True, default=None, blank=True)
    strength = models.IntegerField(null=True, default=None, blank=True)
    defence = models.IntegerField(null=True, default=None, blank=True)
    stamina = models.IntegerField(null=True, default=None, blank=True)
    def __str__(self):
        return f"{self.pokemon} {self.level}"

    class Meta:
        verbose_name_plural = "PokemonEntities"
