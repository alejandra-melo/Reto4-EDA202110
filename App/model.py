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
from DISClib.ADT.graph import gr
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
                    'landing_points': None,
                    'connections': None,  
                    'countrys':None
                   }

        analyzer['landing_points'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareIds) 
        analyzer['countrys'] = mp.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')
         

    

# Funciones para agregar informacion al catalogo


def addLandingConnection(analyzer, origen, destino,distancia):
    """
    Adiciona los landing_points al grafo como vertices y arcos entre las
    landing_points adyacentes.

    Los vertices tienen por nombre el identificador del landing_point
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    try:
        addVertice(analyzer, origen)
        addVertice(analyzer, destino)
        addConnection(analyzer, origen, destino, distancia)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')

# Funciones para creacion de datos

def mapVertice(analyzer, landing_pointId):
    """
    Adiciona un landing point al map
    """
    mp.put(analyzer['landing_points'],landing_pointId['landing_point_id'],landing_pointId)
    None

def addVertice(analyzer, landing_pointId):
    """
    Adiciona una landing_point como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], landing_pointId):
            gr.insertVertex(analyzer['connections'], landing_pointId)
            
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos landing_points
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    existVertice = gr.containsVertex(origin)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    

    return analyzer

def addRouteConnections(analyzer):
    """
    Por cada vertice (cada landing_point) se recorre la lista
    de rutas servidas en dicho landing_point y se crean
    arcos entre ellas para representar el cambio de ruta
    que se puede realizar en una estación.
    """
    lststops = mp.keySet(analyzer['stops'])
    for key in lt.iterator(lststops):
        lstroutes = mp.get(analyzer['stops'], key)['value']
        prevrout = None
        for route in lt.iterator(lstroutes):
            route = key + '-' + route
            if prevrout is not None:
                addConnection(analyzer, prevrout, route, 0)
                addConnection(analyzer, route, prevrout, 0)
            prevrout = route

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
    cont = mp.size(analyzer['landing_points'])
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

def getClustCom(cont, lp1, lp2):
    """
    Retorna el número total de clústeres presentes en 
    la red e informa si los landing points están en el
    mismo clúster o no.
    """
    pass


def getPuntosConex(cont):
    """
    Retorna la lista de landing points (nombre, pais,
    identificador) y el total de cables conectados a 
    dichos landing points.
    """
    pass

def getRutaMenorDist(cont, paisA, paisB):
    """
    Retorna la ruta (incluir la distancia de conexión [km]
    entre cada par consecutivo de landing points) y la
    distancia total de la ruta.
    """
    pass

def getInfraest(cont):
    """
    """
    pass

def getFallas(cont, lp):
    pass

def getMejoresCanales(cont, pais, cable):
    pass

def getMejorRuta(cont, ip1, ip2):
    pass
