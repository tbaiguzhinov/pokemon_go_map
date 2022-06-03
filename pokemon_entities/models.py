from email.base64mime import header_length
from email.policy import default
from tkinter import CASCADE
from django.db import models


class Pokemon(models.Model):
    """Покемон"""
    title = models.CharField("имя", max_length=200)
    title_en = models.CharField(
        "имя на английском",
        max_length=200,
        blank=True
        )
    title_jp = models.CharField("имя на японском", max_length=200, blank=True)
    previous_evolution = models.ForeignKey(
        'self',
        verbose_name='Из кого эволюционирует',
        null=True,
        blank=True,
        related_name='next_evolutions',
        on_delete=models.SET_NULL
        )
    next_evolution = models.ForeignKey(
        'self',
        verbose_name='В кого эволюционирует',
        null=True,
        blank=True,
        related_name='previous_evolutions',
        on_delete=models.SET_NULL
        )
    description = models.TextField("описание", blank=True)
    image = models.ImageField(
        "изображение",
        upload_to="pokemon_images",
        default=None,
        blank=True
        )

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    """Единица Покемона"""
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE,
        verbose_name="Покемон"
        )
    lat = models.FloatField("долгота")
    lon = models.FloatField("широта")
    appeared_at = models.DateTimeField("когда появился", null=True, blank=True)
    disappeared_at = models.DateTimeField("когда исчез", null=True, blank=True)
    level = models.IntegerField(
        "уровень",
        null=True,
        default=None,
        blank=True)
    health = models.IntegerField(
        "здоровье",
        null=True,
        default=None,
        blank=True
        )
    strength = models.IntegerField(
        "сила",
        null=True,
        default=None,
        blank=True
        )
    defence = models.IntegerField(
        "защита",
        null=True,
        default=None,
        blank=True
        )
    stamina = models.IntegerField(
        "выносливость",
        null=True,
        default=None,
        blank=True
        )

    def __str__(self):
        return f"{self.pokemon} {self.level}"

    class Meta:
        verbose_name_plural = "PokemonEntities"
