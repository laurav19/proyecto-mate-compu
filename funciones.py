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

def cuantasFotos(clave, claves):
  """
  Regresa el numero de fotos que existen de una persona dada su clave
  """
  return (claves == clave).sum()

def plotMosaico(img, titulos, alt, anch, nFilas, nColumnas, random):
  """
  Muestra una galeria de nFilas x nColumnas con las imagenes contenidas en el arreglo img
  Asigna a cada imagen uno de los titulos contenidos en el arreglo titulos, cada imagen es de alt x anch
  El parametro random al estar activado selecciona imagenes al azar del arreglo img
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
  Muestra la imagen img, con las medidas alt x anch; le asigna el titulo dado
  """
  plt.imshow(img.reshape((alt, anch)), cmap=plt.cm.gray)
  plt.title(titulo)
  plt.xticks(())
  plt.yticks(())

def matrizAleatoria(m, n, imagenes1D):
  """
  Regresa una matriz de m x n con imagenes del conjunto imagenes1D elegidas aleatoriamente
  """
  arr = np.array(np.arange(m*n), dtype = object)
  nom = np.array(np.arange(m*n), dtype = object)
  for i in range(0, m*n):
    rand = np.random.randint(0,imagenes1D.shape[0])
    arr[i] = imagenes1D[rand]
    nom[i] = ""
  arr.reshape(m,n)
  return arr, nom

def muestraProm(clave, nombres, altura, ancho):
  """
  Muestra el rostro promedio de la persona con la clave dada
  """
  prom = rostroPromTotal(clave)
  tlt = "Rostro promedio " + nombres[clave]
  muestraImagen(prom, altura, ancho, tlt)

def minimoImagenes(claves, nombres, nPersonas, info=False):
  """
  Devuelve el menor numero de imagenes que tienen los personajes
  """
  mi = (claves == 0).sum()
  ind = 0
  for i in range(0,nPersonas):
    if (claves == i).sum() < mi:
      mi = (claves == i).sum()
      ind = i
  if info:
    print "La persona que menor cantidad de fotos tiene es " + nombres[ind] + " con " + str(mi) + " fotos."
  return mi

def arrToMatrix(arrEntre):
  """
  Recibe un arreglo de una dimension con las imagenes de entrenamiento y lo transforma en una matriz de (no_imag, 2914)
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
  Regresa los indices donde se encuentran los n mayores valores de un arreglo
  """
  ind = arr.argsort()[-n:][::-1]
  return ind

def norma(vec):
  """
  Calcula la norma de un vector o arreglo de una dimension
  """
  v = np.asarray(vec)
  norma = ((v**2).sum())**0.5
  return norma

def porAciertoIndividual(clave, conjunto, pruebas, entrenamientos, prediccion):
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
  
def porAciertoIndividualEntrenamiento(clave, entrenamientos, prediccion):
  aci = 0
  for j in range(0, entrenamientos[clave].shape[0]):
    if prediccion(entrenamientos[clave][j]) == clave:
      aci = aci + 1;
  return 100.0*aci/entrenamientos[clave].shape[0]

def resultados1(pruebas, entrenamientos, nEntrenamiento, no_eigC, nPersonas, claves, prediccion):
  suma = 0
  nFotos = 0
  print "RESUTADOS PRIMER METODO"
  print "\nEntrenamiento = " + str(nEntrenamiento)
  print "Eigenvectores = " + str(no_eigC)
  print "\nImagenes de prueba"
  print "\nClave\tCant. prueba\tPorcentaje acierto"
  for i in range (0, nPersonas):
    pruebai = cuantasFotos(i,claves) - nEntrenamiento
    aciertoi = porAciertoIndividual(i, "prueba", pruebas, entrenamientos, prediccion)
    #suma = suma + aciertoi*pruebai
    #nFotos = nFotos + pruebai
    print str(i) + "\t" + str(pruebai) + "\t\t" + str(aciertoi) + "%"
  #suma = suma/nFotos
  #print "\nTotal = " + str(suma) + "%"
  
  print "\n\nImagenes de entrenamiento"
  print "\nClave\tCant. prueba\tPorcentaje acierto"
  for i in range (0, nPersonas):
    pruebai = nEntrenamiento
    aciertoi = porAciertoIndividual(i, "entrenamiento", pruebas, entrenamientos, prediccion)
    #suma = suma + aciertoi*pruebai
    #nFotos = nFotos + pruebai
    print str(i) + "\t" + str(pruebai) + "\t\t" + str(aciertoi) + "%"
  #suma = suma/nFotos
  #print "\nTotal = " + str(suma) + "%"

def porAciertoIndividual2(clave, parametro, conjunto, pruebas, entrenamientos, prediccion2):
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

def resultados2(parametro1, pruebas, entrenamientos, nEntrenamiento, no_eigC, nPersonas, claves, prediccion2):
  suma = 0
  nFotos = 0
  print "RESULTADOS SEGUNDO METODO\n"
  print "\nEntrenamiento = " + str(nEntrenamiento)
  print "Eigenvectores = " + str(no_eigC)
  print "\nConjunto de prueba\n"
  print "Clave\tCant. prueba\tPorcentaje acierto"
  for i in range (0, nPersonas):
    pruebai = cuantasFotos(i, claves) - nEntrenamiento
    aciertoi = porAciertoIndividual2(i, parametro1, "prueba", pruebas, entrenamientos, prediccion2)
    #suma = suma + aciertoi*pruebai
    #nFotos = nFotos + pruebai
    if aciertoi != -1:
      print str(i) + "\t" + str(pruebai) + "\t\t" + str(aciertoi) + "%"
    else:
      print str(i) + "\t" + str(pruebai) + "\t\tdesconocido"
  #suma = suma/nFotos
  
  print "\nConjunto de entrenamiento\n"
  print "Clave\tCant. prueba\tPorcentaje acierto"
  for i in range (0, nPersonas):
    pruebai =  nEntrenamiento
    aciertoi = porAciertoIndividual2(i, parametro1, "entrenamiento", pruebas, entrenamientos, prediccion2)
    #suma = suma + aciertoi*pruebai
    #nFotos = nFotos + pruebai
    if aciertoi != -1:
      print str(i) + "\t" + str(pruebai) + "\t\t" + str(aciertoi) + "%"
    else:
      print str(i) + "\t" + str(pruebai) + "\t\tdesconocido"
  #suma = suma/nFotos
  #print "\nTotal = " + str(suma) + "%"

def imagenInternet(url):
  """
  Regresa un arreglo con una imagen que se puede obtener de una direccion url. Le asigna un formato en blanco y negro de 8 bits
  """
  req = urllib.urlopen(url)
  img = Image.open(StringIO(req.read()))
  img = img.convert(mode = 'L')
  img = np.array(img)
  return img

def muestraPrediccion(imagen, nombre, prediccion, entrenamientos, nombres):
  fig, ax = plt.subplots(1,2, figsize=(5,17))
  plt.gray()
  ax[0].imshow(imagen)
  ax[0].set_title(nombre)
  ax[0].set_axis_off()

  ax[1].imshow(entrenamientos[prediccion][0])
  ax[1].set_title(nombres[prediccion])
  ax[1].set_axis_off()
