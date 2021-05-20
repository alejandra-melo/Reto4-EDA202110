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
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

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
    pass

def getFallas(cont, lp):
    pass

def getMejoresCanales(cont, pais, cable):
    pass

def getMejorRuta(cont, ip1, ip2):
    pass
