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


from DISClib.DataStructures.rbt import keys
import config as cf
import math as mt
from App import model
import csv
from DISClib.ADT import list as lt
from DISClib.DataStructures import arraylist as alt
from DISClib.ADT import map as mp
from DISClib.ADT import queue as q
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import prim
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
        analyzer['countrys'] = mp.newMap(numelements=300,
                                     maptype='PROBING',
                                     comparefunction=compareIds)
        analyzer['landing_points'] = mp.newMap(numelements=1680,
                                     maptype='PROBING',
                                     comparefunction=compareIds)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')
         

    

# Funciones para agregar informacion al catalogo

def addConnection(analyzer, origen, destino, distancia):
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

def crearVertices(analyzer, i, ori):
    
    grafo = analyzer['connections']
    id = ori
    cable = i["cable_name"]
    vertice = id + "-" + cable
    if gr.containsVertex(grafo, vertice) != True:
        gr.insertVertex(grafo,vertice)


def CapitalEstaEnLP(analyzer, capital):
    #mirar si está o no la capital en lp
    encontrado = False
    for lps in lt.iterator(mp.valueSet(analyzer["landing_points"])):
        if encontrado == False:
            if str(capital + ", ") in str(lps["lista"]["elements"][0]["name"]):
                encontrado = True

    return(encontrado)

def AgregarCapital(analyzer):
    nuevo_id = 19250
    for country in lt.iterator(mp.valueSet(analyzer["countries"])):
        c_name = country["lista"]["elements"][0]["CapitalName"]
        if CapitalEstaEnLP(analyzer, c_name) == False:
            nuevo_id += 1
            value = lt.newList('ARRAY_LIST')
            id = country["lista"]["elements"][0]["CountryName"]
            pais = country["lista"]["elements"][0]["CountryName"]
            lat = country["lista"]["elements"][0]["CapitalLatitude"]
            long = country["lista"]["elements"][0]["CapitalLongitude"]
            d = {}
            d['landing_point_id'] = nuevo_id
            d['id'] = id
            d['name'] = c_name + ", " + pais
            d['latitude'] = lat
            d['longitude'] = long
            lt.addLast(value, d)
            mp.put(analyzer["landing_points"], nuevo_id, value)
            gr.insertVertex(analyzer["connections"], nuevo_id)
            conexionCapital(analyzer, country)


def conexionCapital(analyzer, country):
    pass

def unirVertLp(analyzer): 
    """
    Para cada landing point se recuperan todos los vértices del
    mismo landing point con diferente cable. 
    """  
    vert = gr.vertices(analyzer["connections"]) 
    
    for lp in lt.iterator(mp.valueSet(analyzer["landing_points"])):
        v_lp = lt.newList('SINGLE_LINKED')
        for v in lt.iterator(vert):
            num = str.split(v,"-")
            if lp["elements"][0]["landing_point_id"] == num[0]:
                print("****** LO ENCONTRE *******")
                lt.addLast(v_lp, v)
        
        pos = 0
        tam = lt.size(v_lp)
        print("TAMAÑÑÑO")
        print(tam)
        #tam = v_lp['size']
       
        if tam > 1:
            while pos < tam:
                vertexA = lt.getElement(v_lp,pos)
                vertexB = lt.getElement(v_lp,pos+1)
                gr.addEdge(analyzer["connections"], vertexA, vertexB, weight=0.1) 
                pos += 1
            if tam > 2:
                vertexA = lt.getElement(v_lp,0)
                vertexB = lt.getElement(v_lp,tam-1)
                gr.addEdge(analyzer["connections"], vertexA, vertexB, weight=0.1)


def addCountry(analyzer, country):
    key = country['CountryName']
    
    paises = analyzer['countrys']
    value = lt.newList('ARRAY_LIST')
    d = {}
    country_n = country["CountryName"]
    capital_n = country["CapitalName"]
    lat = country["CapitalLatitude"]
    long = country["CapitalLongitude"]
    cc = country["CountryCode"]
    p = country["Population"]
    i_users = country["Internet users"]

    d["CountryName"] = country_n
    d["CapitalName"] = capital_n
    d["CapitalLatitude"] = lat
    d["CapitalLongitude"] = long
    d["CountryCode"] = cc
    d["Population"] = p
    d["Internet users"] = i_users
    lt.addLast(value, d)
    mp.put(paises, key, value)
        

   
def addLandingP(analyzer, vertice):
    lps = analyzer['landing_points']
    value = lt.newList('ARRAY_LIST')
    #vertice es la linea de info
    d = {}
    key = vertice['landing_point_id']
    id = vertice["id"]
    name = vertice["name"]
    lat = vertice["latitude"]
    long = vertice["longitude"]

    d['landing_point_id'] = key
    d['id'] = id
    d['name'] = name
    d['latitude'] = lat
    d['longitude'] = long
    lt.addLast(value, d)
    mp.put(lps, key, value)
    

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

    
def DistGeoLandP(analyzer, origen, destino):
    #1)Obtener la latitud y longitud del origen y destino
    for lps in lt.iterator(mp.valueSet(analyzer["landing_points"])):
        if str(origen) in str(lps["elements"][0]["landing_point_id"]):
            lat_o = lps["elements"][0]["latitude"]
            long_o = lps["elements"][0]["longitude"]
        if str(destino) in str(lps["elements"][0]["landing_point_id"]):
            lat_d = lps["elements"][0]["latitude"]
            long_d = lps["elements"][0]["longitude"]

    #2)Aplicar la función Haversine para calcular las distancias
    rad = mt.pi/180
    f_lat_o = float(lat_o)
    f_lat_d = float(lat_d)
    f_long_o = float(long_o)
    f_long_d = float(long_d)
    dif_lat = f_lat_o - f_lat_d
    dif_long = f_long_o - f_long_d
    r_tierra = 6372.795477598
    a = (mt.sin(rad*dif_lat)/2)**2 + mt.cos(rad*f_lat_d) * mt.cos(rad*f_lat_o) * (mt.sin(rad*dif_long)/2)**2
    distancia = 2 * r_tierra * mt.asin(mt.sqrt(a))

    return(distancia)


# Funciones de ordenamiento

def VNombreaNum(analyzer, lp):
    
    for lps in lt.iterator(mp.valueSet(analyzer["landing_points"])):
        if str(lp) in str(lps["elements"][0]["name"]):
            id_lp = lps["elements"][0]["landing_point_id"]
    
    return(id_lp)


def VNumaNombre(analyzer, lp):
    
    for lps in lt.iterator(mp.valueSet(analyzer["landing_points"])):
        if str(lp) in str(lps["elements"][0]["landing_point_id"]):
            id_lp = lps["elements"][0]["name"]
    
    return(id_lp)


def getClustCom(analyzer, lp1, lp2):
    """
    Retorna el número total de clústeres presentes en 
    la red e informa si los landing points están en el
    mismo clúster o no.
    """
    sccs = scc.KosarajuSCC(analyzer["connections"])

    #recorrer tabla de landing points y buscar los ids
    id_lp1 = VNombreaNum(analyzer, lp1)
    id_lp2 = VNombreaNum(analyzer, lp2)
    vert = gr.vertices(analyzer["connections"])
    e1 = False
    e2 = False

    for v in lt.iterator(vert):
        if e1 == True and e2 == True:
            break
        num = str.split(v,"-")
        if id_lp1 == num[0]:
            vertice1 = v
            e1 = True
        elif id_lp2 == num[0]:
            vertice2 = v 
            e2 = True

    print(vertice1)
    print(vertice2)

    clusters = scc.connectedComponents(sccs)
    mismo_c = scc.stronglyConnected(sccs, vertice1, vertice2)

    return (clusters, mismo_c)

def getPuntosConex(analyzer):
    """
    Retorna la lista de landing points (nombre, pais,
    identificador) y el total de cables conectados a 
    dichos landing points.
    """
    vert = gr.vertices(analyzer["connections"]) 
    max = 0
    lista_max = lt.newList('ARRAY_LIST')
    for lp in lt.iterator(mp.valueSet(analyzer["landing_points"])):
        l_v = lt.newList('ARRAY_LIST')
        for v in lt.iterator(vert):
            num = str.split(v,"-")
            if lp["elements"][0]["landing_point_id"] == num[0]:
                lt.addLast(l_v, v)
        calc_cables = lt.size(l_v)
        if calc_cables > max:
            max = calc_cables
            lista_max = lt.newList('ARRAY_LIST')
            lt.addLast(lista_max, lp["elements"][0]["landing_point_id"])
        elif calc_cables == max:
            lt.addLast(lista_max, lp["elements"][0]["landing_point_id"])

    return(lista_max, max)
        

def buscaCapital(analyzer, pais):
    for country in lt.iterator(mp.valueSet(analyzer["countrys"])):
        if pais == country["lista"]["elements"][0]["CountryName"]:
            capital = country["lista"]["elements"][0]["CapitalName"]

    return(capital)
           


def getRutaMenorDist(analyzer, paisA, paisB):
    """
    Retorna la ruta (incluir la distancia de conexión [km]
    entre cada par consecutivo de landing points) y la
    distancia total de la ruta.
    """
    #encontrar la capital
    cap_A = buscaCapital(analyzer, paisA)
    cap_B = buscaCapital(analyzer, paisB)

    #encontrar landing_point de la capital y lo devuelve como id
    vertixA = VNombreaNum(analyzer, cap_A)
    vertixB = VNombreaNum(analyzer, cap_B)

    search = djk.Dijkstra(analyzer["connections"], vertixA)
    assert djk.hasPathTo(search, vertixB) is True
    path = djk.pathTo(search, vertixB)
    distancia = djk.distTo(search, vertixB)

    return (path, distancia)


def getInfraest(analyzer):
    """
    Identificar la red de expansión minima en cuanto a
    distancia que pueda darle cobertura a la mayor cantidad
    de landing points. Retorna: # de nodos conectados a la
    red de expansion minima (camino de menor costo que 
    conecta la mayor cantidad de nodos), costo total de la
    red de expansión minima y presentar la rama mas larga
    (mayor numero de arcos entre raiz y la hoja que hace parte
    de la red de expansion minima).
    """
    mst = prim.PrimMST(analyzer["connections"])
    #valores = gr.edges(mst)
    #num_v = q.size(mst["mst"])
    #num_v = gr.numEdges(mst['edgeTo'])
    peso = prim.weightMST(analyzer["connections"], mst)
    print(peso)
    #print(mst)
    print(mst["mst"])

    return(num_v, peso)


def getFallas(analyzer, lp):
    """
    Se requiere conocer la lista de países que podrían verse
    afectados al producirse una caída en el proceso de
    comunicación con dicho landing point; los países afectados
    son aquellos que cuentan con landing points directamente
    conectados con el landing point afectado. 
    """
    id_lp = VNombreaNum(analyzer, lp)
    p_afect = gr.adjacents(analyzer["connections"], id_lp)
    dist_p = gr.adjacentEdges(analyzer["connections"], id_lp)
    #ordenar la lista según distancia mayor a menor
    num_p = gr.degree(analyzer["connections"], id_lp)

    return(p_afect, num_p)


def getMejoresCanales(analyzer, pais, cable):
    pass

def getMejorRuta(analyzer, ip1, ip2):
    pass

