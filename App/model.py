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
from App import model
import csv
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.ADT.graph import gr
from DISClib.ADT import stack as st
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newAnalyzer():
    """ Inicializa el analizador

   landing_points: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar los puntos de conexion 
   components: Almacena la informacion de los componentes conectados
   countrys:  Tabla de hash que almacena los paises cargados y su informacion  
    """
    try:
        analyzer = {
                    'connections': None,  
                    'countrys':None
                   }

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareIds) 
        analyzer['countrys'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareIds)
        analyzer['landing_points'] = mp.newMap(numelements=1280,
                                     maptype='PROBING',
                                     comparefunction=compareIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')
         

    

# Funciones para agregar informacion al catalogo


def addConnection(analyzer, origen, destino,distancia, connection):
    """
    Crea conexiones entre landing points (arcos)
    """
    grafo = analyzer['connections']
    try:
        gr.addEdge(grafo,origen,destino,distancia)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addConnection')

# Funciones para creacion de datos

def crearVertices(analyzer, landing_pointId):
    
    grafo = analyzer['connections']
    vertice = landing_pointId['landing_point_id']
     
    gr.insertVertex(grafo,vertice)

    

def addCountry(analyzer, country):
    paises = analyzer['countrys']
    key = country['CountryName']
    esta = mp.contains(paises, key)
    if esta:
        entry = mp.get(paises,key)
        value = me.getValue(entry)
        lt.addLast(value['lista'], country)
    else:
        pais = newCountry(key)
        lista = pais['lista']
        lt.addLast(lista,country)
        mp.put(paises,key,pais)

    

def newCountry(name):
    """
    Define la estructura de un pais 
    """
    country = { 'name' : name, 'lista': None}
    country['lista'] = lt.newList('ARRAY_LIST')
    return country


def addLandingP(analyzer, vertice):
    
    lps = analyzer['landing_points']
    key = vertice['landing_point_id']
    esta = mp.contains(lps, key)
    if esta:
        entry = mp.get(lps,key)
        value = me.getValue(entry)
        lt.addLast(value['lista'], vertice)
    else:
        lp = newLandingP(key)
        lista = lp['lista']
        lt.addLast(lista, vertice)
        mp.put(lps,key,lp)


def newLandingP(id):
    """
    Define la estructura de un landing point 
    """
    lp = { 'id' : id, 'lista': None}
    lp['lista'] = lt.newList('ARRAY_LIST')
    return lp


# Funciones de consulta

def numeroPaises(analyzer):

    """
    Retorna el numero de paises unicos
    """
    cont = mp.size(analyzer['countrys'])
    return cont


def numeroPoints(analyzer):
    """
    Retorna el numero de landing points
    """
    cont = gr.numVertices(analyzer['connections'])
    return cont

def totalConexiones(analyzer):
    """
    Retorna el numero de arcos entre landing points
    """
    cont = gr.numEdges(analyzer['connections'])
    return cont 


# Funciones utilizadas para comparar elementos dentro de una lista

def compareIds(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1

# Funciones de ordenamiento

def getClustCom(analyzer, lp1, lp2):
    """
    Retorna el número total de clústeres presentes en 
    la red e informa si los landing points están en el
    mismo clúster o no.
    """
    sccs = scc.KosarajuSCC(analyzer["connections"])
    #recorrer tabla de landing points y buscar los ids

    for lp in lt.iterator(mp.valueSet(analyzer["landing_points"])):
        if str(lp1) in str(lp["lista"]["elements"][0]["name"]):
            id_lp1 = lp["lista"]["elements"][0]["landing_point_id"]
        elif str(lp2) in str(lp["lista"]["elements"][0]["name"]):
            id_lp2 = lp["lista"]["elements"][0]["landing_point_id"]

    clusters = scc.sccCount(analyzer["connections"], sccs, id_lp1)
    numero = clusters["idscc"]
    mismo_c = scc.stronglyConnected(sccs, id_lp1, id_lp2)
    print(numero)

    return (clusters, mismo_c)

def getPuntosConex(analyzer):
    """
    Retorna la lista de landing points (nombre, pais,
    identificador) y el total de cables conectados a 
    dichos landing points.
    """
    max = 0
    lista_max = lt.newList('ARRAY_LIST')
    
    for lp in lt.iterator(mp.valueSet(analyzer["landing_points"])):
        vertex = lp["lista"]["elements"][0]["landing_point_id"]
        calc_arcos = gr.degree(analyzer["connections"], vertex)
        if calc_arcos > max:
            max = calc_arcos
            lista_max = lt.newList('ARRAY_LIST')
            lt.addLast(lista_max, vertex)
        elif calc_arcos == max:
            lt.addLast(lista_max, vertex)

    return(lista_max, max)

def getRutaMenorDist(analyzer, paisA, paisB):
    """
    Retorna la ruta (incluir la distancia de conexión [km]
    entre cada par consecutivo de landing points) y la
    distancia total de la ruta.
    """
    #encontrar la capital y cambiar vértice de id a nombre
    search = djk.Dijkstra(analyzer["connections"], paisA)
    assert djk.hasPathTo(search, paisB) is True
    path = djk.pathTo(search, paisB)
    distancia = djk.distTo(search, paisB)

    return (path, distancia)


def getInfraesnalyzer():
    """
    """
    pass

def getFallas(analyzer, lp):
    pass

def getMejoresCanales(analyzer, pais, cable):
    pass

def getMejorRuta(analyzer, ip1, ip2):
    pass



