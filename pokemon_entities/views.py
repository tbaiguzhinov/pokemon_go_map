from urllib.error import HTTPError
import folium
import json
import logging

from django.http import Http404, HttpResponseNotFound
from django.utils.timezone import localtime
from django.shortcuts import render, get_object_or_404
from pokemon_entities.models import Pokemon, PokemonEntity

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=localtime(),
        disappeared_at__gte=localtime(),
    )

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    pokemons = Pokemon.objects.all()

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'title_ru': pokemon.title,
            'img_url': request.build_absolute_uri(pokemon.image.url)
            if pokemon.image else "",
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon_record = get_object_or_404(Pokemon, id=pokemon_id)
    pokemon = {
        "title_ru": pokemon_record.title,
        "description": pokemon_record.description,
        "title_en": pokemon_record.title_en,
        "title_jp": pokemon_record.title_jp,
        "img_url": request.build_absolute_uri(pokemon_record.image.url),
    }
    previous_evolution = pokemon_record.previous_evolution
    if previous_evolution:
        pokemon["previous_evolution"] = {
            "pokemon_id": previous_evolution.id,
            "img_url": request.build_absolute_uri(
                previous_evolution.image.url
            ),
            "title_ru": previous_evolution.title
        }
    next_evolutions = pokemon_record.next_evolutions.all()
    if next_evolutions:
        pokemon["next_evolutions"] = []
        for next_evolution in next_evolutions:
            pokemon["next_evolutions"].append(
                {
                    "pokemon_id": next_evolution.id,
                    "img_url": request.build_absolute_uri(
                        next_evolution.image.url
                    ),
                    "title_ru": next_evolution.title,
                })
    pokemon_entities = PokemonEntity.objects.filter(pokemon__id=pokemon_id)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url),
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
