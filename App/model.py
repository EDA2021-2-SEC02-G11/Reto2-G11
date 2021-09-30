"""
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
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import mergesort as mer
assert cf
from datetime import datetime
import time

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""
# Construccion de modelos

def newCatalog():
    """
    Inicializa el catálogo de obras de arte. 
    Crea listas vacías con los siguientes própositos:
    Para guardar las obras de arte
    Para guardar los autores
    Quizá luego se añaden más listas con los autores ordenados o lo que se necesite.
    """
    catalog = {'artists_BeginDate': None,
               'artworks_DateAcquired': None,
               'artworks_Date': None,
               'artworks_Artist':None,
               'nationality':None,
               'mediums':None}
    
    catalog['artists_BeginDate'] = lt.newList('ARRAY_LIST', cmpfunction=compareArtists_BeginDate)
    catalog['artworks_DateAcquired'] = lt.newList('ARRAY_LIST', cmpfunction=compareArtworks_DateAcquired)
    catalog['artworks_Date'] = lt.newList('ARRAY_LIST', cmpfunction=compareArtworks_Date)
    catalog['artworks_Artist'] = lt.newList('ARRAY_LIST', cmpfunction=compareArtworks_Artist)
    catalog['nationality'] = lt.newList('ARRAY_LIST', cmpfunction=compareNationality)
    
    """
    LAB 5: Este índice crea un map cuya llave es el medio o técnica con el que se realizó la obra
    """
    catalog['mediums'] = mp.newMap(21251, # Número de medios distintos en el large, que será el número de llaves
                                   maptype='CHAINING',
                                   loadfactor=4.0,
                                   comparefunction=compareMediums)

    return catalog

# Funciones para agregar informacion al catalogo

def addArtist(catalog, artist):
    lt.addLast(catalog['artists_BeginDate'], artist)
    ids=artist["Nationality"]
    
def addMedium(catalog, mediumkey, artwork):
    """
    Esta función adiciona un medio o técnica al map de medios.
    Cuando se adiciona el medio se actualiza la cantidad de obras de dicho medio.
    """
    mediums = catalog['mediums']
    existmedium = mp.contains(catalog['mediums'], mediumkey)
    if existmedium:
        entry = mp.get(catalog['mediums'], mediumkey)
        mediumvalue = me.getValue(entry)
    else:
        mediumvalue = newMedium(mediumkey)
        mp.put(catalog['mediums'], mediumkey, mediumvalue)
    lt.addLast(mediums['artworks'], artwork)
    mediums['amount'] += 1    

def addArtwork(catalog, artwork):
    """
    Esta función adiciona un obra a la lista de obras,
    Lo guarda en un Map usando como llave su medio.
    """
    lt.addLast(catalog['artworks_DateAcquired'], artwork)
    lt.addLast(catalog['artworks_Date'], artwork)
    mp.put(catalog['mediums'], artwork['Medium'], artwork)
    ids = artwork['ConstituentID']
    ids = ids[1:-1].split(",")
    for id_ in ids:
        id_ = int(id_.strip())
        addArtworks_Artist(catalog, id_, artwork)
        addNationality(catalog,id_,artwork)

def addArtworks_Artist(catalog, id_:int, artwork):
    artist_artwork = catalog['artworks_Artist']
    posartist = lt.isPresent(artist_artwork, id_)
    if posartist > 0:
        artist_id = lt.getElement(artist_artwork, posartist)
    else:
        artist_id = newArtworks_Artist(id_)
        lt.addLast(artist_artwork, artist_id)
    lt.addLast(artist_id['artworks'],artwork )

def addNationality(catalog, id_, artwork):
    nationality = catalog['nationality']
    nation=id_nation(catalog,id_)
    posnationality = lt.isPresent(nationality, nation)
    if posnationality > 0:
        nation_id = lt.getElement(nationality, posnationality)
    else:
        nation_id = newNationality(nation)
        lt.addLast(nationality, nation_id)
    lt.addLast(nation_id['artworks'],artwork )

# Funciones para creacion de datos

# LAB 5: 
def newMedium(medium):
    """
    Crea una nueva estructura para modelar los medios o técnicas de una obra. 
    Se crea una lista para las obras de dicho medio.
    """
    mediums = {'medium': '',
              'artworks': None,
              'amount': 0}
    mediums['name'] = medium
    mediums['artworks'] = lt.newList('SINGLE_LINKED', compareMediums)
    return mediums
# ----

def newArtworks_Artist(id_):
    """
    Crea una nueva estructura para modelar las obras por autor.
    """
    answ = {'artist':"",'artworks':None}
    answ['artist'] = id_
    answ['artworks'] = lt.newList('ARRAY_LIST')
    return answ

def newNationality(nation):
    """
    Crea una nueva estructura para modelar los autores de cada obra
    """
    nationality = {'nation':"",'artworks':None}
    nationality['nation'] = nation
    nationality['artworks'] = lt.newList('ARRAY_LIST')
    return nationality

# Funciones de consulta

# Req. 1
def rangoArtists(catalog, anio1, anio2):
    artists = catalog["artists_BeginDate"].copy()
    start_time = time.process_time()
    start=float("inf")
    pos=1
    while pos<=lt.size(artists):
        if int(lt.getElement(artists,pos)["BeginDate"])>=anio1:
            start=pos
            break
        pos+=1
    initial=start
    num=0
    while start<=lt.size(artists):
        if int(lt.getElement(artists,start)["BeginDate"])<=anio2:
            num+=1
        else:
            break
        start+=1
    answ = lt.subList(artists,initial,num)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return answ

# Req. 2
def rangoArtworks(catalog, fecha1, fecha2):
    artworks = catalog["artworks_DateAcquired"].copy()
    start_time = time.process_time()
    start=float("inf")
    pos=1
    while pos<=lt.size(artworks):
        if lt.getElement(artworks,pos)["DateAcquired"] != "":
            if datetime.strptime(lt.getElement(artworks,pos)["DateAcquired"], '%Y-%m-%d').date()>=datetime.strptime(fecha1, '%Y-%m-%d').date():
                start=pos
                break
        pos+=1
    initial=start
    num=0
    while start<=lt.size(artworks):
        if datetime.strptime(lt.getElement(artworks,start)["DateAcquired"], '%Y-%m-%d').date()<=datetime.strptime(fecha2, '%Y-%m-%d').date():
            num+=1
        else:
            break
        start+=1
    answ = lt.subList(artworks,initial,num)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return answ

# Req. 3
def id_artist(catalog, artist):
    """
    reorna el id de un artista. O(n)
    """
    id_=0
    for i in lt.iterator(catalog['artists_BeginDate']):
        if i['DisplayName']==artist:
            id_ = i['ConstituentID']
            break
    return id_,artist

def artist_artworks(catalog, artist):
    """
    Nombre, ID y lista de las obras de un artista determinado. O(n)
    """
    id_=id_artist(catalog, artist) # ID del artista
    artworks_by_artist=lt.newList('ARRAY_LIST',key='ObjectID')
    for i in lt.iterator(catalog['artworks_DateAcquired']):
        if id_ in i['ConstituentID'][1:-1].split(","):
            lt.addLast(artworks_by_artist, i)
    return artworks_by_artist,artist,id_

def artist_medium1(catalog, artist):
    mediums= lt.newList('ARRAY_LIST')
    mediums_count = lt.newList('ARRAY_LIST')
    id_,artist=id_artist(catalog, artist)
    for i in lt.iterator(catalog['artworks_Artist']):
        if int(i['artist']) == int(id_):
            artworks_by_artist=i['artworks']
            break
    for i in lt.iterator(artworks_by_artist):
        posmedium = lt.isPresent(mediums, i['Medium'])
        if posmedium <= 0: # Si no está el medio en la lista de medios
            lt.addLast(mediums, i['Medium'])
            lt.addLast(mediums_count, 1)
        else: # Si sí está el medio en la lista de medios
            lt.changeInfo(mediums_count, posmedium, lt.getElement(mediums_count, posmedium)+1)
    greatest=0
    pos_actual=0
    for cuenta_medium in lt.iterator(mediums_count):
        pos_actual+=1
        if cuenta_medium > greatest:
            greatest=cuenta_medium
            pos_most_used=pos_actual
    artworks_medium= lt.newList('ARRAY_LIST')        
    for obra in lt.iterator(artworks_by_artist):
        if obra['Medium']==lt.getElement(mediums,pos_most_used):
            lt.addLast(artworks_medium, obra)
    return artist,id_,artworks_by_artist,mediums,artworks_medium,pos_most_used

# Req. 4

def id_nation(catalog, ids):
    """
    retorna la nacion de un artista. O(n)
    """
    for i in lt.iterator(catalog['artists_BeginDate']):
        if int(i['ConstituentID'])==int(ids):
            artist = i["Nationality"]
            if artist=="" or artist=="Nationality unknown":
                artist="Unknown"
            break
    return artist

# Req. 5

def departament_artworks(catalog, department):
    """
    ObjectID de las obras de un departamento determinado. 
    Ya ordenadas por fecha.
    """
    artworks_by_department=lt.newList('ARRAY_LIST',key='ObjectID')
    for i in lt.iterator(catalog['artworks_Date']):
        if i['Department'] == department:
            lt.addLast(artworks_by_department, i)              
    return artworks_by_department,department

def condicion(medida):
    """
    Si la medida no existe o es 0, que sea 1 para que no afecte la multiplicación.
    """
    try:
        medida=int(medida)
    except:
        medida=0
    medida=medida/100 # Divido en 100 para pasar a metros
    return medida
    
def transport(catalog, department):
    artworks_by_department,department=departament_artworks(catalog, department)
    precios_obras=lt.newList('ARRAY_LIST')
    for obra in lt.iterator(artworks_by_department):
#         O la obra es circular o tiene longitudes:
        d1=condicion(obra['Depth (cm)'])
        d2=condicion(obra['Height (cm)'])
        d3=condicion(obra['Length (cm)'])
        d4=condicion(obra['Width (cm)'])
        if d1!=0:
            metros=d1
        else:
            d1=1 # Si es 0, lo cambio a 1 para que no afecte la multiplicación de ahorita
            if d2!=0:
                metros=d2
            else:
                d2=1
                if d3!=0:
                    metros=d3
                else:
                    d3=1
                    if d4!=0:
                        metros=d4
                    else:
                        d4=1
                        metros=0 # Metros es 0 si y sólo si todos son 0
        if metros!=0: # Alguno no es 0
            metros=d1*d2*d3*d4      
#       La obra puede ser circular
        if condicion(obra['Circumference (cm)']) != 1:
            circ=condicion(obra['Circumference (cm)'])
            radio = circ/(6.28318530718) # Circ/2pi = r
            area = 3.141592*(radio)**2
        elif condicion(obra['Diameter (cm)']) != 1: # Depronto toca con el diametro
            d = condicion(obra['Diameter (cm)'])
            area = 3.141592*(d/2)**2
        else: # No es circular
            area=0
        try:
            peso = int(obra['Weight (kg)'])
        except:
            peso=0.        
        if peso==0. and area==0 and metros==0: # Ninguna está
            precio_obra = 48.00
        else: # alguna está
            mas_grande= max([peso,area,metros])
            precio_obra = 72.00*mas_grande
        lt.addLast(precios_obras,precio_obra)
    precio_final=0
    for precio in lt.iterator(precios_obras):
        precio_final+=precio
    return artworks_by_department,department,precios_obras,precio_final,peso


# Funciones utilizadas para comparar elementos dentro de una lista

#LAB 5:

def compareMediums(keyname,medium):
    """
    Compara dos medios. El primero es una cadena
    y el segundo un entry de un map
    """
    mediumentry = me.getKey(medium)
    if (keyname == mediumentry):
        return 0
    elif (keyname > mediumentry):
        return 1
    else:
        return -1
    
#---

def compareArtworks_DateAcquired(artwork1:dict , artwork2:dict)->int:
    if artwork1["DateAcquired"]=="" or artwork2["DateAcquired"]=="":
        if artwork1["DateAcquired"]=="":
            return -1
        else:
            return 0
    elif datetime.strptime(artwork1["DateAcquired"], '%Y-%m-%d').date()<datetime.strptime(artwork2["DateAcquired"], '%Y-%m-%d').date():
        return -1
    return 0

def compareArtists_BeginDate(artist1,artist2):
    if artist1["BeginDate"]<=artist2["BeginDate"]:
        return -1
    else:
        return 0

def compareArtworks_Artist(artist_id, artist):
    if artist_id == artist['artist']:
        return 0
    return -1
    
def compareArtworks_Date(artwork1,artwork2):
    """
    Por antiguedad. Deja las que no tienen fecha al final.
    """
    if artwork1["Date"]=="" or artwork2["Date"]=="":
        if artwork1["Date"]=="":
            return 0
        return -1
    elif artwork1["Date"]<=artwork2["Date"]:
        return -1
    return 0

def compareNationality(artist_id, artist):
    if artist_id == artist['nation']:
        return 0
    return -1

def compareNationality2(nation1, nation2):
    if lt.size(nation1["artworks"]) < lt.size(nation2["artworks"]):
        return -1
    return 0

# Funciones de ordenamiento

def sortArtists_BeginDate(catalog):
    sub_list = catalog["artists_BeginDate"].copy()
    start_time = time.process_time()
    sorted_list= mer.sort(sub_list, compareArtists_BeginDate)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list

def sortArtworks_DateAcquired(catalog):
    sub_list = catalog["artworks_DateAcquired"].copy()
    start_time = time.process_time()
    sorted_list= mer.sort(sub_list, compareArtworks_DateAcquired)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list

def sortArtworks_Date(catalog):
    sub_list = catalog["artworks_Date"].copy()
    start_time = time.process_time()
    sorted_list= mer.sort(sub_list, compareArtworks_Date)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list

def sortNationality(catalog):
    sub_list = catalog["nationality"].copy()
    start_time = time.process_time()
    sorted_list= mer.sort(sub_list, compareNationality2)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    return elapsed_time_mseg, sorted_list