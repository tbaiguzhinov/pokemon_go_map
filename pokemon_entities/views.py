import folium
import json

from django.http import HttpResponseNotFound
from django.utils.timezone import localtime
from django.shortcuts import render
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
    current_time = localtime()
    pokemon_entities = PokemonEntity.objects.filter(
        appeared_at__lte=current_time,
        disappeared_at__gte=current_time,
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
            'img_url': request.build_absolute_uri(pokemon.image.url) if pokemon.image else "",
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon_record = Pokemon.objects.get(id=pokemon_id)
    pokemon = {"title_ru": pokemon_record.title,
    #"title_en": ,
    #"title_jp": ,
    "img_url": request.build_absolute_uri(pokemon_record.image.url),
    #"previous_evolution": ,
    #"next_evolution": ,
    }

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
