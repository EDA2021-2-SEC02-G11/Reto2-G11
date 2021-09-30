"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
assert cf
import time
from prettytable import PrettyTable

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    """
    Imprime las opciones del menú.
    """
    print("\nMenú de opciones:\n")
    print("0. Cargar información en el catálogo.")
    print("Req. No. 1. Listar cronológicamente los artistas.")
    print("Req. No. 2. Listar cronológicamente las adquisiciones.")
    print("Req. No. 3. Clasificar las obras de un artista por técnica.")
    print("Req. No. 4. Clasificar las obras por la nacionalidad de sus creadores.")
    print("Req. No. 5. Transportar obras de un departamento.")
    print("Req. No. 6 (Bono). Proponer una nueva exposición en el museo.")
    print("7. Req. Lab5. n obras más antiguas para un medio específico.")
    print("8. Detener la ejecución del programa.")
    
def printloadData():
    print("Cargando información de los archivos ....")
    catalog = initCatalog()
    loadData(catalog)
    artist=controller.sortArtists_BeginDate(catalog)
    artwork=controller.sortArtworks_DateAcquired(catalog)
    artwork_date=controller.sortArtworks_Date(catalog)
    nationality=controller.sortNationality(catalog)
    catalog["artists_BeginDate"]=artist[1]
    catalog["artworks_DateAquired"]=artwork[1]
    catalog["artworks_Date"]=artwork_date[1]
    catalog["nationality"]=nationality[1]
    print('Número de artistas en el catálogo: ',
          str(lt.size(catalog['artists_BeginDate'])))
    print('Número de obras de arte en el catálogo: ',
          str(lt.size(catalog['artworks_DateAquired'])))
    print("Se demoro: ",str(artist[0]))
    print('\nÚltimos tres artistas cargados:\n')
    answ = PrettyTable(['Nombre','Nacimiento','Fallecimiento'
                        ,'Nacionalidad','Género'])
    for i in [-2,-1,0]:        
        answ.add_row([lt.getElement(catalog['artists_BeginDate'],i)['DisplayName'],
                      lt.getElement(catalog['artists_BeginDate'],i)['BeginDate'],
                      lt.getElement(catalog['artists_BeginDate'],i)['EndDate'],
                      lt.getElement(catalog['artists_BeginDate'],i)['Nationality'],
                      lt.getElement(catalog['artists_BeginDate'],i)['Gender']])
    answ._max_width = {'Nombre':40}
    print(answ)
    print("Se demoro: ",str(artwork[0]))
    print('\nÚltimas tres obras de arte cargadas:\n')
    answ1 = PrettyTable(['Título','Medio o técnica','Fecha'
                        ,'Adquisición','Dimensiones'])
    for i in [-2,-1,0]:       
        answ1.add_row([lt.getElement(catalog['artworks_DateAcquired'],i)['Title'],
                      lt.getElement(catalog['artworks_DateAcquired'],i)['Medium'],
                      lt.getElement(catalog['artworks_DateAcquired'],i)['Date'],
                      lt.getElement(catalog['artworks_DateAcquired'],i)['DateAcquired'],
                      lt.getElement(catalog['artworks_DateAcquired'],i)['Dimensions']])
    answ1._max_width = {'Título':40,'Medio o técnica':20,'Fecha':20,'Adquisición':40,
                        'Dimensiones':40}
    print(answ1)
    return catalog
    
def printReq1():
    anio1=int(input("Digite un año inicial: "))
    anio2=int(input("Digite un año final: "))
    start_time = time.process_time()
    result=controller.rangoArtists(catalog, anio1, anio2)
    print("======================== Req No. 1 Inputs ========================")
    print("Artistas nacidos entre ",str(anio1)," y ",str(anio2)),"."
    print("======================== Req No. 1 Respuesta ========================")
    print("Hay ",str(lt.size(result))," artistas nacidos entre ",
          str(anio1)," y ",str(anio2)),"."
    print('\nPrimeros y últimos tres artistas nacidos en el rango de años:\n')
    answ = PrettyTable(['Nombre','Nacimiento','Fallecimiento'
                        ,'Nacionalidad','Género'])
    for i in [1,2,3,-2,-1,0]:        
        answ.add_row([lt.getElement(result,i)['DisplayName'],
                      lt.getElement(result,i)['BeginDate'],
                      lt.getElement(result,i)['EndDate'],
                      lt.getElement(result,i)['Nationality'],
                      lt.getElement(result,i)['Gender']])
    answ._max_width = {'Nombre':40}
    print(answ)  
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print("Se demoro: ",str(elapsed_time_mseg))
    
def printReq2():
    fecha1=input("Ingrese una fecha inicial en formato AAAA-MM-DD: ")
    fecha2=input("Ingrese una fecha final en formato AAAA-MM-DD: ")
    start_time = time.process_time()
    result = controller.rangoArtworks(catalog, fecha1, fecha2)
    num_artists = 5 # TODO: FALTA Toca asociar con los artistas para esto
    num_purchased = 5 # TODO: Falta
    print("======================== Req No. 1 Inputs ========================")
    print("Obras adquiridas entre ",fecha1," y ",fecha2)
    print("======================== Req No. 1 Respuesta ========================")
    print("El MoMA adquirió ",str(lt.size(result))," obras entre ",fecha1,
          " y ",fecha2," con ",str(num_artists),
          " artistas, de las cuales compró ",str(num_purchased))
    print('\nPrimeras y últimas tres obras adquiridas en el rango de fechas:\n')
    answ = PrettyTable(['Título','Artista(s)','Fecha','Adquisición','Medio',
                        'Dimensiones'])
    for i in [1,2,3,-2,-1,0]:        
        answ.add_row([lt.getElement(result,i)['Title'],
                      lt.getElement(result,i)['ConstituentID'], # TODO: Artista
                      lt.getElement(result,i)['Date'],
                      lt.getElement(result,i)['DateAcquired'],
                      lt.getElement(result,i)['Medium'],
                      lt.getElement(result,i)['Dimensions']])
    answ._max_width = {'Título':40,'Artista(s)':20,'Fecha':15,'Adquisición':15,
                       'Medio':20,'Dimensiones':40}
    print(answ)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print("Se demoro: ",str(elapsed_time_mseg))
    
def printReq3():
    artist=input("Ingrese el nombre del artista: ")
    start_time = time.process_time()
    artist,id_,artworks_by_artist,mediums,artworks_medium,pos_most_used=controller.artist_medium1(catalog,artist)
    print("======================== Req No. 3 Inputs ========================")
    print("Examinar el trabajo del artista de nombre: ",artist)
    print("======================== Req No. 3 Respuesta ========================")
    print("El artista "+str(artist).strip()+' con código '+str(id_).strip()+' tiene '+
          str(lt.size(artworks_by_artist)).strip()+' obras en el MoMA.')
    print('Usó '+str(lt.size(mediums)).strip()+' medios o técnicas distintas en su trabajo.')
    print('La técnica que más usó es: '+str(lt.getElement(mediums,pos_most_used)).strip()+'. La usó en '+str(lt.size(artworks_medium)).strip()+' obras')
    print('El listado de las obras de dicha técnica es: ')
    answ1 = PrettyTable(['Título','Fecha','Adquisición',
                         'Medio o técnica','Dimensiones'])
    for i in lt.iterator(artworks_medium):       
        answ1.add_row([i['Title'],i['Date'],i['DateAcquired'],i['Medium'],
                      i['Dimensions']])
    answ1._max_width = {'Título':40,'Medio o técnica':20,'Fecha':20,'Adquisición':40,
                        'Dimensiones':40}
    print(answ1)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print("Se demoro: ",str(elapsed_time_mseg))
    
def printReq4(catalog):
    start_time = time.process_time()
    print("======================== Req No. 4 Inputs ========================")
    print("Ranking de paises por su numero de obras en el MoMa ")
    print("======================== Req No. 4 Respuesta ========================")
    print("Top 10 paises en el MoMa son:")
    answ = PrettyTable(['Nacionalidad','Obras'])
    for i in [0,-1,-2,-3,-4,-5,-6,-7,-8,-9]:
        answ.add_row([lt.getElement(catalog['nationality'],i)['nation'],
                      lt.size(lt.getElement(catalog['nationality'],i)['artworks'])])
    answ._max_width = {'Título':40,'Obras':20}
    print(answ)
    mejor=lt.getElement(catalog['nationality'],0)
    print("La nacionalidad top en el museo es ", mejor["nation"], " con ",lt.size(mejor["artworks"]))
    print("Las primeras y ultimos 3 objetos para las obras de ",mejor["nation"]," son:")
    answ = PrettyTable(['ID','Titulo',"Nombre del artista","Medium","Fecha",
                        "Dimensiones","Departamento","Clasificacion","URL"])
    for i in [1,2,3,-2,-1,0]:
        answ.add_row([lt.getElement(mejor["artworks"],i)['ObjectID'],
                      lt.getElement(mejor["artworks"],i)['Title'],
                      lt.getElement(mejor["artworks"],i)['ConstituentID'],
                      lt.getElement(mejor["artworks"],i)['Medium'],
                      lt.getElement(mejor["artworks"],i)['Date'],
                      lt.getElement(mejor["artworks"],i)['Dimensions'],
                      lt.getElement(mejor["artworks"],i)['Department'],
                      lt.getElement(mejor["artworks"],i)['Classification'],
                      lt.getElement(mejor["artworks"],i)['URL']])
    answ._max_width = {'ID':20,'Titulo':40,"Nombre del artista":20,"Medium":20,
                    "Fecha":20,"Dimensiones":20,"Departamento":20,"Clasificacion":20,"URL":40}
    print(answ)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print("Se demoro: ",str(elapsed_time_mseg))
    
def printReq5():
    department=input("Ingrese el nombre del departamento: ")
    start_time = time.process_time()
    artworks_by_department,department,precios_obras,precio_final,peso=controller.transport(catalog, department)
    print("======================== Req No. 5 Inputs ========================")
    print('Estime el costo de transportar todas las obras del departamento '+department+' del MoMA.')
    print("======================== Req No. 5 Respuesta ========================")
    print('El MoMA transportará '+str(lt.size(artworks_by_department)).strip()
          +' obras del departamento '+str(department)+'.')
    print('El precio estimado del servicio es: $'+str(precio_final).strip()+' USD.')
    print('El peso estimado de todas las obras es de: '+str(peso)+' kg.')
    print("Las cinco obras más antiguas que se van a transportar son: ")
    answ = PrettyTable(['Título','Artista(s)','Clasificacion','Fecha','Medio',
                        'Dimensiones','Costo'])
    result=artworks_by_department
    for i in [1,2,3,4,5]:        
        answ.add_row([lt.getElement(result,i)['Title'],
                      lt.getElement(result,i)['ConstituentID'], # TODO: Artista
                      lt.getElement(result,i)['Classification'],
                      lt.getElement(result,i)['Date'],
                      lt.getElement(result,i)['Medium'],
                      lt.getElement(result,i)['Dimensions'],
                      lt.getElement(precios_obras,i)])
    answ._max_width = {'Título':40,'Artista(s)':20,'Fecha':15,'Adquisición':15,
                       'Medio':20,'Dimensiones':40,'Costo':15}
    print(answ)
    print("Las cinco obras más costosas que se van a transportar son: ")
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print("Se demoro: ",str(elapsed_time_mseg))
    
def printReq6():
    print("Este requerimiento aún no se ha implementado.")
    
def printReqLab5():
    medio=input("Ingrese el nombre del medio o técnica: ")
    n=int(input("Ingrese el número de obrtas que desea consultar: "))
    print("======================== Req Lab5 Inputs ========================")
    print('Mostrar las '+str(n)+' obras más antiguas para el medio '+medio+'.')
    print("======================== Req Lab5 Respuesta ========================")
    print('Las '+str(n)+' obras más antiguas para el medio '+medio+' son:')
    llave_valor = mp.get(catalog['mediums'], medio)
    valor = me.getValue(llave_valor)
    print('El medio '+str(medio)+' tiene en total '+str(valor['amount'])+' obras.')
    print(lt.subList(valor['artworks'],1,n))
    
def initCatalog():
    """
    Inicializa el catalogo de libros
    """
    return controller.initCatalog()

def loadData(catalog):
    """
    Carga los libros en la estructura de datos
    """
    controller.loadData(catalog)

catalog = None

"""
Menú principal
"""
while True:
    error = "\nError: Por favor ingrese un número entero entre 0 y 7.\n"
    error_cargar= "\nError: Se deben cargar los datos antes de usar los requisitos.\n"
    printMenu()
    try:
        inputs = int(input('Seleccione una opción para continuar: \n'))
    except:
        print(error)
        continue
    if inputs == 0:
        catalog=printloadData()
    elif inputs>0 and inputs<8:
        if type(catalog)!=dict:
            print(error_cargar)
        elif inputs==1:
            printReq1()
        elif inputs==2:
            printReq2()
        elif inputs==3:
            printReq3()
        elif inputs==4:
            printReq4(catalog)
        elif inputs==5:
            printReq5()
        elif inputs==6:
            printReq6()
        elif inputs==7:
            printReqLab5()
    elif inputs >= 9:
        print(error)
    else:
        sys.exit(0)
sys.exit(0)