﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
import time
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mer
from datetime import datetime
assert cf


# Construcción de modelos


def newCatalog():
    """
    Inicializa el catálogo de obras de arte.
    """
    catalog = {}

    catalog['artists'] = lt.newList('ARRAY_LIST', key='ConstituentID')
    catalog['artworks'] = lt.newList('ARRAY_LIST', key='ConstituentID')

    # Requirement 1

    catalog['artistsByBeginDate'] = mp.newMap(21251,  # TODO: N. 'BeginDate' la
                                              maptype='PROBING',
                                              loadfactor=0.2,
                                              comparefunction=compareKeys)

    # Requirement 3

    catalog['mediumsByArtist'] = mp.newMap(21251,  # TODO: N. 'Medium' large
                                           maptype='PROBING',
                                           loadfactor=0.2,
                                           comparefunction=compareKeys)

    # Requirement 4

    catalog['nationalities'] = mp.newMap(119,  # N. nationalities in 'large'
                                         maptype='PROBING',
                                         loadfactor=0.2,
                                         comparefunction=compareKeys)

    # LAB 5. key: 'Medium', value: array of artworks by medium.

    catalog['mediums'] = mp.newMap(21251,  # Number of mediums in 'large' file.
                                   maptype='PROBING',
                                   loadfactor=0.2,
                                   comparefunction=compareKeys)

    # LAB 6. key: 'Nationality', value: array of artworks by nationality.

    catalog['nationalities'] = mp.newMap(119,  # N. nationalities in 'large'
                                         maptype='PROBING',
                                         loadfactor=0.2,
                                         comparefunction=compareKeys)

    return catalog

# Funciones para agregar información al catalogo invocadas por controller.py


def addArtist(catalog, artist):
    addArtistByBeginDate(catalog, artist)
    lt.addLast(catalog['artists'], artist)


def addArtwork(catalog, artwork):
    """
    Esta función adiciona un obra a la lista de obras,
    Lo guarda en un Map usando como llave su medio.
    """
    lt.addLast(catalog['artworks'], artwork)
    ids = artwork['ConstituentID']
    ids = ids[1:-1].split(",")
    for id_ in ids:
        id_ = int(id_.strip())
        addNationality(catalog, id_, artwork)
    addMedium(catalog, artwork['Medium'], artwork)

# Requirement 1


def addArtistByBeginDate(catalog, artist):
    """
    Adds a new artist to artistsByBeginDate map.
    """
    begin_date = int(artist['BeginDate'])
    begin_date_exists = mp.contains(catalog['artistsByBeginDate'], begin_date)
    if begin_date_exists:
        entry = mp.get(catalog['artistsByBeginDate'], begin_date)
        artists_of_begin_date = me.getValue(entry)
    else:
        artists_of_begin_date = newBeginDateArray(artist)
        mp.put(catalog['artistsByBeginDate'], begin_date,
               artists_of_begin_date)
    lt.addLast(artists_of_begin_date, artist)


def newBeginDateArray(artist):
    """
    Creates new array for artists born in the same year
    """
    begin_date_array = lt.newList('ARRAY_LIST', compareKeys)
    return begin_date_array


def requirement1(catalog, initial_year, final_year):
    count = 0
    muestra = lt.newList('ARRAY_LIST', key='BeginDate')
    year_0 = initial_year-1
    while year_0 <= final_year and lt.size(muestra) < 3:
        year_0 += 1
        entry = mp.get(catalog['artistsByBeginDate'], year_0)
        print(entry)
        if entry:
            artists_by_year = me.getValue(entry)
            count += lt.size(artists_by_year)
            i = 1
            while i <= lt.size(artists_by_year):
                artist = lt.getElement(artists_by_year, i)
                lt.addLast(muestra, artist)
                if lt.size(muestra) >= 3:
                    break
                i += 1 
    year_f = final_year+1
    while year_f >= initial_year and lt.size(muestra) < 6:
        year_f -= 1
        entry = mp.get(catalog['artistsByBeginDate'], year_f)
        artists_by_year = me.getValue(entry)
        count += lt.size(artists_by_year)
        i = lt.size(artists_by_year)
        while i > 0:            
            artist = lt.getElement(artists_by_year, i)
            lt.addLast(muestra, artist)
            if lt.size(muestra) >= 6:
                break
            i -= 1
    for year in range(year_0+1, year_f):
        entry = mp.get(catalog['artistsByBeginDate'], year)
        artists_by_year = me.getValue(entry)
        count += lt.size(artists_by_year)
    return count, muestra


# LAB 5


def addMedium(catalog, mediumkey, artwork):
    """
    Esta función adiciona un medio o técnica al map de medios.
    Cuando se adiciona el medio se actualiza la cantidad de obras de dicho medio.
    """
    existmedium = mp.contains(catalog['mediums'], mediumkey)
    if existmedium:
        entry = mp.get(catalog['mediums'], mediumkey)
        mediumvalue = me.getValue(entry)
    else:
        mediumvalue = newMedium(mediumkey)
        mp.put(catalog['mediums'], mediumkey, mediumvalue)
    lt.addLast(mediumvalue['artworks'], artwork)
    mediumvalue['size'] += 1


def newMedium(medium):
    """
    Crea una nueva estructura para modelar los medios o técnicas de una obra. 
    Se crea una lista para las obras de dicho medio.
    """
    mediums = {'medium': '',
               'artworks': None,
               'size': 0}
    mediums['medium'] = medium
    mediums['artworks'] = lt.newList('ARRAY_LIST', key='Date')
    return mediums

# LAB 6


def addNationality(catalog, id_, artwork):
    """
    Adds a new nationality to nationalities map.
    """
    nationality_key = id_nation(catalog, id_)
    nationality_exists = mp.contains(catalog['nationalities'], nationality_key)
    if nationality_exists:
        entry = mp.get(catalog['nationalities'], nationality_key)
        nationality_value = me.getValue(entry)
    else:
        nationality_value = newNationality(nationality_key)
        mp.put(catalog['nationalities'], nationality_key, nationality_value)
    lt.addLast(nationality_value['artworks'], artwork)
    nationality_value['size'] += 1


def id_nation(catalog, ids):
    """
    retorna la nacion de un artista. O(n)
    """
    for i in lt.iterator(catalog['artists']):
        if int(i['ConstituentID']) == int(ids):
            artist = i["Nationality"]
            if artist == "" or artist == "Nationality unknown":
                artist = "Unknown"
            break
    return artist


def newNationality(nationality):
    """
    Creates structure with array of all artworks with artists
    that share nationality
    """
    nationality_value = {'nationality': '',
                         'artworks': None,
                         'size': 0}
    nationality_value['nationality'] = nationality
    nationality_value['artworks'] = lt.newList('ARRAY_LIST', key='Date')
    return nationality_value


def compareArtworksByDate(artwork1, artwork2):
    """
    Por antiguedad. Deja las que no tienen fecha al final.
    """
    if artwork1["Date"] == "" or artwork2["Date"] == "":
        if artwork1["Date"] == "":
            return 0
        return -1
    elif artwork1["Date"] <= artwork2["Date"]:
        return -1
    return 0


# Funciones de comparación genéricas

def compareKeys(key, entry):
    """
    Compares key with entry

    keyname: string
    entry: map entry (dict)
    """
    entry_key = me.getKey(entry)
    if key == entry_key:
        return 0
    elif key > entry_key:
        return 1
    else:
        return -1


# Funciones de ordenamiento


def sortAntiguedad(lista):
    sorted_list = mer.sort(lista, compareArtworksByDate)
    return sorted_list