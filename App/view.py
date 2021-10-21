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
import time
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from prettytable import PrettyTable
assert cf


def printMenu():
    """
    Imprime las opciones del menú.
    """
    print("\nMenú de opciones:\n")
    print("0. Cargar información en el catálogo.")
    print("Req. No. 1. Listar cronológicamente los artistas.")
    print("Req. No. 2. Listar cronológicamente las adquisiciones.")
    print("Req. No. 3. Clasificar las obras de un artista por técnica.")
    print("""Req. No. 4. Clasificar las obras por la nacionalidad de sus
          creadores.""")
    print("Req. No. 5. Transportar obras de un departamento.")
    print("Req. No. 6 (Bono). Proponer una nueva exposición en el museo.")
    print("7. Req. Lab5. n obras más antiguas para un medio específico.")
    print("8. Req. Lab6. número de obras de una nacionalidad.")
    print("9. Detener la ejecución del programa.")


def printloadData():
    print("Cargando información de los archivos...")
    start_time = time.process_time()
    catalog = initCatalog()
    loadData(catalog)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print('Número de artistas en el catálogo: ' +
          str(lt.size(catalog['artists'])))
    print('Número de obras de arte en el catálogo: ' +
          str(lt.size(catalog['artworks'])))
    print('\nÚltimos tres artistas cargados:\n')
    answ = PrettyTable(['Nombre', 'Nacimiento', 'Fallecimiento',
                        'Nacionalidad', 'Género'])
    for i in [-2, -1, 0]:
        answ.add_row([lt.getElement(catalog['artists'], i)['DisplayName'],
                      lt.getElement(catalog['artists'], i)['BeginDate'],
                      lt.getElement(catalog['artists'], i)['EndDate'],
                      lt.getElement(catalog['artists'], i)['Nationality'],
                      lt.getElement(catalog['artists'], i)['Gender']])
    answ._max_width = {'Nombre': 40}
    print(answ)
    print('\nÚltimas tres obras de arte cargadas:\n')
    answ1 = PrettyTable(['Título', 'Medio o técnica', 'Fecha', 'Adquisición',
                         'Dimensiones'])
    for i in [-2, -1, 0]:
        answ1.add_row([lt.getElement(catalog['artworks'], i)['Title'],
                      lt.getElement(catalog['artworks'], i)['Medium'],
                      lt.getElement(catalog['artworks'], i)['Date'],
                      lt.getElement(catalog['artworks'], i)['DateAcquired'],
                      lt.getElement(catalog['artworks'], i)['Dimensions']])
    answ1._max_width = {'Título': 40, 'Medio o técnica': 20, 'Fecha': 20,
                        'Adquisición': 40, 'Dimensiones': 40}
    print(answ1)
    print("La función de cargar datos demoró "+str(elapsed_time_mseg)+' ms.')
    return catalog


def printReq1():
    initial_year = int(input("Digite un año inicial: "))
    final_year = int(input("Digite un año final: "))
    start_time = time.process_time()
    count, muestra = controller.requirement1(catalog, initial_year, final_year)
    print("========================= Req No. 1 Inputs =======================")
    print("Artistas nacidos entre "+str(initial_year)+" y "+str(final_year) +
          '.')
    print("======================== Req No. 1 Respuesta =====================")
    print("Hay "+str(count)+" artistas nacidos entre "+str(initial_year) +
          " y "+str(final_year)+".")
    print('\nPrimeros y últimos tres artistas nacidos en el rango de años:\n')
    answ = PrettyTable(['Nombre', 'Nacimiento', 'Fallecimiento', 
                        'Nacionalidad', 'Género'])
    for i in [1, 2, 3, 0, -1, -2]:
        answ.add_row([lt.getElement(muestra, i)['DisplayName'],
                      lt.getElement(muestra, i)['BeginDate'],
                      lt.getElement(muestra, i)['EndDate'],
                      lt.getElement(muestra, i)['Nationality'],
                      lt.getElement(muestra, i)['Gender']])
    answ._max_width = {'Nombre': 40}
    print(answ)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print("Se demoró: "+str(elapsed_time_mseg))


def printReq2():
    fecha1 = input("Ingrese una fecha inicial en formato AAAA-MM-DD: ")
    fecha2 = input("Ingrese una fecha final en formato AAAA-MM-DD: ")
    start_time = time.process_time()
    count, muestra = controller.requirement2(catalog, fecha1, fecha2)
    print("======================== Req No. 2 Inputs ========================")
    print("Obras adquiridas entre "+fecha1+" y "+fecha2)
    print("======================== Req No. 2 Respuesta =====================")
    print("El MoMA adquirió "+str(count)+" obras entre "+fecha1+'y'+fecha2+".")
          # de las cuales compró ",str(num_purchased))
    print('\nPrimeras y últimas tres obras adquiridas en el rango de fechas:\n')
    answ = PrettyTable(['Título','Artista(s)','Fecha','Adquisición','Medio',
                        'Dimensiones'])
    for i in [1,2,3,0,-1,-2]:        
        answ.add_row([lt.getElement(muestra, i)['Title'],
                      controller.getArtistFromID(catalog,
                      lt.getElement(muestra, i)['ConstituentID']),
                      lt.getElement(muestra, i)['Date'],
                      lt.getElement(muestra, i)['DateAcquired'],
                      lt.getElement(muestra, i)['Medium'],
                      lt.getElement(muestra, i)['Dimensions']])
    answ._max_width = {'Título':20,'Artista(s)':20,'Fecha':15,'Adquisición':15,
                       'Medio':20,'Dimensiones':20}
    print(answ)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print("Se demoró: ",str(elapsed_time_mseg))


def printReq3():
    artist = input("Ingrese el nombre del artista: ")
    start_time = time.process_time()
    number_of_artworks, number_of_mediums, most_used, times_used, muestra = controller.requirement3(catalog, artist)
    print("======================= Req No. 3 Inputs =========================")
    print("Examinar el trabajo del artista de nombre: "+artist)
    print("====================== Req No. 3 Respuesta =======================")
    print("El artista "+artist+' tiene '+str(number_of_artworks)
          +' obras en el MoMA.')
    print('Usó '+str(number_of_mediums)+' medios o técnicas distintas en su trabajo.')
    print('La técnica que más usó es: '+str(most_used)+'. La usó en '+str(times_used)+' obras')
    print('El listado de las obras de dicha técnica es: ')
    print('\nPrimeras y últimas tres obras adquiridas en el rango de fechas:\n')
    answ = PrettyTable(['Título','Fecha','Adquisición','Medio',
                        'Dimensiones'])
    for i in [1,2,3,0,-1,-2]:        
        answ.add_row([lt.getElement(muestra, i)['Title'],
                      lt.getElement(muestra, i)['Date'],
                      lt.getElement(muestra, i)['DateAcquired'],
                      lt.getElement(muestra, i)['Medium'],
                      lt.getElement(muestra, i)['Dimensions']])
    answ._max_width = {'Título':20,'Fecha':15,'Adquisición':15,
                       'Medio':20,'Dimensiones':20}
    print(answ)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print("Se demoró: ",str(elapsed_time_mseg))


def printReq4(catalog):
    mayor = controller.requirement4(catalog)
    print("======================== Req No. 4 Inputs ========================")
    print("Ranking de paises por el numero de obras en el MoMA")
    print("======================== Req No. 4 Respuesta =====================")
    print("El top 10 de paises en el MoMA son:")
    print('\nPrimeras y últimas tres obras adquiridas en el rango de fechas:\n')
    print(mayor)


def printReq5():
    department = input("Ingrese el nombre del departamento: ")
    start_time = time.process_time()
    artworks, precios_obras, precio, peso = controller.requirement5(catalog, department)
    print("======================= Req No. 5 Inputs =========================")
    print('Estime el costo de transportar todas las obras del departamento '+
          department+' del MoMA.')
    print("====================== Req No. 5 Respuesta =======================")
    print('El MoMA transportará '+str(lt.size(artworks)).strip()+
          ' obras del departamento '+department+'.')
    print('El precio estimado del servicio es: $'+str(precio).strip() +
          ' USD.')
    print('El peso estimado de todas las obras es de: '+str(peso)+' kg.')
    print("Las cinco obras más costosas que se van a transportar son: ")
    print("Las cinco obras más antiguas que se van a transportar son: ")
    answ = PrettyTable(['Título', 'Artista(s)', 'Clasificacion', 'Fecha',
                        'Medio', 'Dimensiones', 'Costo'])
    result=artworks
    for i in [1,2,3,4,5]:
        answ.add_row([lt.getElement(result, i)['Title'],
                      controller.getArtistFromID(catalog,
                      lt.getElement(result, i)['ConstituentID']),
                      lt.getElement(result, i)['Classification'],
                      lt.getElement(result, i)['Date'],
                      lt.getElement(result, i)['Medium'],
                      lt.getElement(result, i)['Dimensions'],
                      lt.getElement(precios_obras, i)])
    answ._max_width = {'Título': 20, 'Artista(s)': 20, 'Fecha': 15,
                       'Adquisición': 15, 'Medio': 20, 'Dimensiones': 20,
                       'Costo': 15}
    print(answ)
    stop_time = time.process_time()
    elapsed_time_mseg = (stop_time - start_time)*1000
    print("Se demoró: "+str(elapsed_time_mseg))


def printReq6():
    print("Este requerimiento aún no se ha implementado.")


def printReqLab5():
    medio = input("Ingrese el nombre del medio o técnica: ")
    n = int(input("Ingrese el número de obras que desea consultar: "))
    print("======================== Req Lab5 Inputs =========================")
    print('Mostrar las '+str(n)+' obras más antiguas para el medio '+medio+'.')
    print("====================== Req Lab5 Respuesta ========================")
    llave_valor = mp.get(catalog['mediums'], medio)
    valor = me.getValue(llave_valor)
    sorteada = controller.sortAntiguedad(valor['artworks'])
    print('El medio '+str(medio)+' tiene en total '+str(valor['size'])+
          ' obras.')
    print('Las '+str(n)+' obras más antiguas para el medio '+medio+' son:')
    answ = PrettyTable(['Título', 'Clasificacion', 'Fecha', 'Medio',
                        'Dimensiones'])
    result = lt.subList(sorteada, 1, n)
    i = 1
    while i <= n:
        answ.add_row([lt.getElement(result, i)['Title'],
                      lt.getElement(result, i)['Classification'],
                      lt.getElement(result, i)['Date'],
                      lt.getElement(result, i)['Medium'],
                      lt.getElement(result, i)['Dimensions']])
        i+=1
    answ._max_width = {'Título':40,'Fecha':15,'Adquisición':15,
                       'Medio':20,'Dimensiones':40}
    print(answ)


def printReqLab6():
    nacionalidad=input("Ingrese la nacionalidad: ")
    print("======================== Req Lab5 Inputs ========================")
    print("""Contar el número total de obras de una nacionalidad utilizando el 
            índice creado por la propiedad "Nationality". """)
    print("======================== Req Lab5 Respuesta ========================")
    llave_valor = mp.get(catalog['nationalities'], nacionalidad)
    valor = me.getValue(llave_valor)
    print('La nacionalidad '+str(nacionalidad)+' tiene en total '+
          str(valor['size'])+' obras.')


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
    error = "\nError: Por favor ingrese un número entero entre 0 y 8.\n"
    error_cargar= "\nError: Se deben cargar los datos antes de usar los requisitos.\n"
    printMenu()
    try:
        inputs = int(input('Seleccione una opción para continuar: \n'))
    except:
        print(error)
        continue
    if inputs == 0:
        catalog=printloadData()
    elif inputs>0 and inputs<9:
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
        elif inputs==8:
            printReqLab6()
    elif inputs >= 10:
        print(error)
    else:
        sys.exit(0)
sys.exit(0)