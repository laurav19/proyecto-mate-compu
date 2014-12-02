import pylab
import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg
import os
import sklearn.metrics as skm
from PIL import Image
from sklearn.datasets import fetch_lfw_people
import urllib
from StringIO import StringIO

def cuantasFotos(clave):
  """
  Regresa el número de fotos que existen de una persona dada su clave
  """
  return (claves == clave).sum()

def plotMosaico(img, titulos, alt, anch, nFilas, nColumnas, random):
  """
  Muestra una galería de nFilas x nColumnas con las imágenes contenidas en el arreglo img
  Asigna a cada imagen uno de los títulos contenidos en el arreglo titulos, cada imagen es de alt x anch
  El parámetro random al estar activado selecciona imágenes al azar del arreglo img
  """
  plt.figure(figsize=(1.7 * nColumnas, 2.3 * nFilas))
  plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.35)
  for i in range(nFilas * nColumnas):
    plt.subplot(nFilas, nColumnas, i + 1)
    if random:
      random = np.random.randint(0, img.shape[0])
      plt.imshow(img[random].reshape((alt, anch)), cmap=plt.cm.gray)
      if titulos != np.array([]):
        plt.title(titulos[random], size=12)
    else:
      plt.imshow(img[i].reshape((alt, anch)), cmap=plt.cm.gray)
      if titulos != np.array([]):
        plt.title(titulos[i], size=12)
    plt.xticks(())
    plt.yticks(())

def muestraImagen(img, alt, anch, titulo):
  """
  Muestra la imagen img, con las medidas alt x anch; le asigna el título dado
  """
  plt.imshow(img.reshape((alt, anch)), cmap=plt.cm.gray)
  plt.title(titulo)
  plt.xticks(())
  plt.yticks(())

def matrizAleatoria(m, n):
  """
  Regresa una matriz de m x n con imágenes del conjunto imagenes1D elegidas aleatoriamente
  """
  arr = np.array(np.arange(m*n), dtype = object)
  nom = np.array(np.arange(m*n), dtype = object)
  for i in range(0, m*n):
    rand = np.random.randint(0,imagenes1D.shape[0])
    arr[i] = imagenes1D[rand]
    nom[i] = ""
  arr.reshape(m,n)
  return arr, nom

def muestraProm(clave):
  """
  Muestra el rostro promedio de la persona con la clave dada
  """
  prom = rostroPromTotal(clave)
  tlt = "Rostro promedio " + nombres[clave]
  muestraImagen(prom, altura, ancho, tlt)

def minimoImagenes(info=false):
  """
  Devuelve el menor número de imágenes que tienen los personajes
  """
  mi = (claves == 0).sum()
  ind = 0
  for i in range(0,nPersonas):
    if (claves == i).sum() < mi:
      mi = (claves == i).sum()
      ind = i
  if info:
    print "La persona que menor número de imágenes tiene es " + nombres[ind] + " con " + str(mi) + " imágenes."
  return mi

def arrToMatrix(arrEntre):
  """
  Recibe un arreglo de una dimensión con las imágenes de entrenamiento y lo transforma en una matriz de (no_imag, 2914)
  """
  arr = arrEntre
  s = arr.shape[0]
  resp = np.zeros(62*47*s)
  for i in range(0, s):
    arr[i] = arr[i].reshape(62*47,1)
  for i in range(0,s):
    for j in range(0, 62*47):
      resp[i*62*47 + j] = arr[i][j]
  return np.asmatrix(resp.reshape(s, 62*47))

def indicesMayores(arr, n):
  """
  Regresa los índices donde se encuentran los n mayores valores de un arreglo
  """
  ind = arr.argsort()[-n:][::-1]
  return ind

def norma(vec):
  """
  Calcula la norma de un vector o arreglo de una dimensión
  """
  v = np.asarray(vec)
  norma = ((v**2).sum())**0.5
  return norma

def porAciertoIndividual(clave, conjunto):
  aci = 0
  resp = 0
  if (conjunto == "prueba"):
    for j in range(0, pruebas[clave].shape[0]):
      if prediccion(pruebas[clave][j]) == clave:
        aci = aci + 1;
    resp = 100.0*aci/pruebas[clave].shape[0]
  else:
    if (conjunto == "entrenamiento"):
      for j in range(0, entrenamientos[clave].shape[0]):
        if prediccion(entrenamientos[clave][j]) == clave:
          aci = aci + 1;
      resp = 100.0*aci/entrenamientos[clave].shape[0]
  return resp
  
def porAciertoIndividualEntrenamiento(clave):
  aci = 0
  for j in range(0, entrenamientos[clave].shape[0]):
    if prediccion(entrenamientos[clave][j]) == clave:
      aci = aci + 1;
  return 100.0*aci/entrenamientos[clave].shape[0]

def porAciertoIndividual2(clave, parametro, conjunto):
  aci = 0
  desc = 0
  if (conjunto == "prueba"):
    for j in range(0, pruebas[clave].shape[0]):
      pred = prediccion2(pruebas[clave][j], parametro)
      if pred == -1:
        desc = desc + 1
      else:
        if pred == clave:
          aci = aci + 1;
    if desc == pruebas[clave].shape[0]:
      resp = -1
    else:
      resp = 100.0*aci/(pruebas[clave].shape[0] - desc)
  else:
    if conjunto == "entrenamiento":
      for j in range(0, entrenamientos[clave].shape[0]):
        pred = prediccion2(entrenamientos[clave][j], parametro)
        if pred == -1:
          desc = desc + 1
        else:
          if pred == clave:
            aci = aci + 1;
      if desc == entrenamientos[clave].shape[0]:
        resp = -1
      else:
        resp = 100.0*aci/(entrenamientos[clave].shape[0] - desc)
  return resp

def imagenInternet(url):
  u"""
  Regresa un arreglo con una imagen que se puede obtener de una dirección url. Le asigna un formato en blanco y negro de 8 bits
  """
  req = urllib.urlopen(url)
  img = Image.open(StringIO(req.read()))
  img = img.convert(mode = 'L')
  img = array(img)
  return img

