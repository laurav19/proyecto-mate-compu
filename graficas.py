from IPython.html.widgets import interact, fixed
from IPython.html import widgets
from IPython.display import display
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def derivadasA(estado, t, a, b, z):
  dh = -b*estado[0]*estado[1]
  dz = b*estado[0]*estado[1] + z*estado[2] - a*estado[0]*estado[1]
  dm = a*estado[0]*estado[1] - z*estado[2]
  return np.array([dh, dz, dm])

def graficaSolucionA(humanos, zombies, muertos, a, b, z):
  tiempo = np.linspace(0, 2, 1000)
  estadoA = np.array([humanos, zombies,muertos])
  sol = odeint(derivadasA,estadoA, tiempo, args=(a, b, z))
  plt.figure(figsize=(15,5))
  plt.plot(tiempo,sol.T[0], c='b', label="Humanos", linewidth=2)
  plt.plot(tiempo,sol.T[1], c='g', label="Zombies", linewidth=2)
  plt.plot(tiempo,sol.T[2], c='r', label="Muertos")
  lim = np.amax(sol)
  plt.title("Modelo basico", fontweight='bold')
  plt.xlabel("Tiempo (semanas)")
  plt.legend()
  plt.ylim(0,lim+10)

def interactA():
  widH = widgets.IntSliderWidget(min=0,max=1000,step=1,value=100)
  widZ = widgets.IntSliderWidget(min=0,max=1000,step=1,value=1)
  wida = widgets.FloatSliderWidget(min=0.01,max=1,step=0.01,value=0.05)
  widb = widgets.FloatSliderWidget(min=0.1,max=1,step=0.05,value=0.3)
  widz = widgets.FloatSliderWidget(min=0.01,max=0.5,step=0.01,value=0.2)
  interact(graficaSolucionA,humanos=widH, zombies=widZ, muertos=fixed(0), a=wida, b=(0.1,1,0.05), z=(0.01,0.5,0.01));

def derivadasB(estado, t, a, b, z, r):
  dh = -b*estado[0]*estado[2]
  di = b*estado[0]*estado[2] - r*estado[1]
  dz = r*estado[1] + z*estado[3] - a*estado[0]*estado[2]
  dm = a*estado[0]*estado[2] - z*estado[3]
  return np.array([dh, di, dz, dm])

def solucionB(humanos, infectados, zombies, muertos, a, b, z, r):
  tiempo = np.linspace(0, 2, 1000)
  estadoB = np.array([humanos,infectados,zombies,muertos])
  sol = odeint(derivadasB, estadoB, tiempo, args=(a, b, z, r))
  plt.figure(figsize=(15,5))
  plt.plot(tiempo,sol.T[0], c='b', label="Humanos", linewidth=2)
  plt.plot(tiempo,sol.T[2], c='g', label="Zombies", linewidth=2)
  plt.plot(tiempo,sol.T[1], c='purple', label="Infectados")
  plt.plot(tiempo,sol.T[3], c='r', label="Muertos")
  lim = np.amax(sol)
  plt.title("Modelo con infeccion latente", fontweight='bold')
  plt.xlabel("Tiempo (semanas)")
  plt.legend()
  plt.ylim(0,lim+10)

def interactB():
  widH = widgets.IntSliderWidget(min=0,max=1000,step=1,value=100)
  widZ = widgets.IntSliderWidget(min=0,max=1000,step=1,value=1)
  widI = widgets.IntSliderWidget(min=0,max=10,step=1,value=0)
  wida = widgets.FloatSliderWidget(min=0.01,max=1,step=0.01,value=0.05)
  widb = widgets.FloatSliderWidget(min=0.1,max=1,step=0.05,value=0.6)
  widz = widgets.FloatSliderWidget(min=0.01,max=0.5,step=0.01,value=0.2)
  widr = widgets.FloatSliderWidget(min=0.1,max=1,step=0.05,value=0.9)
  interact(solucionB,humanos=widH, infectados=widI, zombies=widZ, muertos=fixed(0), a=wida, b=widb, z=widz, r=widr);

def derivadasC(estado, t, a, b, z, r, k, s, g):
  dh = -b*estado[0]*estado[2]
  di = b*estado[0]*estado[2] - r*estado[1] - k*estado[1]
  dz = r*estado[1] + z*estado[3] - a*estado[0]*estado[2] - s*estado[2]
  dm = a*estado[0]*estado[2] - z*estado[3] + g*estado[4]
  dq = k*estado[1] + s*estado[2] - g*estado[4]
  return np.array([dh, di, dz, dm, dq])

def solucionC(humanos, infectados, zombies, muertos, cuarentena, a, b, z, r, k, s, g):
  tiempo = np.linspace(0, 2, 1000)
  estadoC = np.array([humanos,infectados,zombies,muertos,cuarentena])
  sol = odeint(derivadasC, estadoC, tiempo, args=(a, b, z, r, k, s, g))
  plt.figure(figsize=(15,5))
  plt.plot(tiempo,sol.T[0], c='b', label="Humanos", linewidth=2)
  plt.plot(tiempo,sol.T[2], c='g', label="Zombies", linewidth=2)
  plt.plot(tiempo,sol.T[1], c='purple', label="Infectados")
  plt.plot(tiempo,sol.T[3], c='r', label="Muertos")
  plt.plot(tiempo,sol.T[4], c='c', label="Cuarentena")
  lim = np.amax(sol)
  plt.title("Modelo con cuarentena", fontweight='bold')
  plt.xlabel("Tiempo (semanas)")
  plt.legend()
  plt.ylim(0,lim+10)

def interactC():
  widH = widgets.IntSliderWidget(min=0,max=1000,step=1,value=100)
  widZ = widgets.IntSliderWidget(min=0,max=1000,step=1,value=1)
  widI = widgets.IntSliderWidget(min=0,max=10,step=1,value=0)
  wida = widgets.FloatSliderWidget(min=0.01,max=1,step=0.01,value=0.05)
  widb = widgets.FloatSliderWidget(min=0.1,max=1,step=0.05,value=0.85)
  widz = widgets.FloatSliderWidget(min=0.01,max=0.5,step=0.01,value=0.09)
  widr = widgets.FloatSliderWidget(min=0.1,max=1,step=0.05,value=0.8)
  widk = widgets.FloatSliderWidget(min=0.1,max=1,step=0.1,value=0.3)
  wids = widgets.FloatSliderWidget(min=0.01,max=0.5,step=0.01,value=0.01)
  widg = widgets.FloatSliderWidget(min=0.1,max=1,step=0.1,value=0.6)
  interact(solucionC,humanos=widH, infectados=widI, zombies=widZ, muertos=fixed(0), cuarentena=fixed(0), a=wida, b=widb, z=widz, r=widr, k=widk, s=wids, g=widg);

def derivadasD(estado, t, a, b, z, r, c):
  dh = -b*estado[0]*estado[2] + c*estado[1]
  di = b*estado[0]*estado[2] - r*estado[1] - c*estado[1]
  dz = r*estado[1] + z*estado[3] - a*estado[0]*estado[2]
  dm = a*estado[0]*estado[2] - z*estado[3]
  return np.array([dh, di, dz, dm])

def solucionD(humanos, infectados, zombies, muertos, a, b, z, r, c):
  tiempo = np.linspace(0, 2, 1000)
  estadoD = np.array([humanos,infectados,zombies,muertos])
  sol = odeint(derivadasD, estadoD, tiempo, args=(a, b, z, r, c))
  plt.figure(figsize=(15,5))
  plt.plot(tiempo,sol.T[0], c='b', label="Humanos", linewidth=2)
  plt.plot(tiempo,sol.T[2], c='g', label="Zombies", linewidth=2)
  plt.plot(tiempo,sol.T[1], c='purple', label="Infectados")
  plt.plot(tiempo,sol.T[3], c='r', label="Muertos")
  lim = np.amax(sol)
  plt.title("Modelo con tratamiento", fontweight='bold')
  plt.xlabel("Tiempo (semanas)")
  plt.legend()
  plt.ylim(0,lim+10)

def interactD():
  widH = widgets.IntSliderWidget(min=0,max=1000,step=1,value=100)
  widZ = widgets.IntSliderWidget(min=0,max=1000,step=1,value=1)
  widI = widgets.IntSliderWidget(min=0,max=10,step=1,value=0)
  wida = widgets.FloatSliderWidget(min=0.01,max=1,step=0.01,value=0.05)
  widb = widgets.FloatSliderWidget(min=0.1,max=1,step=0.05,value=0.7)
  widz = widgets.FloatSliderWidget(min=0.01,max=0.5,step=0.01,value=0.5)
  widr = widgets.FloatSliderWidget(min=0.1,max=1,step=0.05,value=0.95)
  widc = widgets.FloatSliderWidget(min=0,max=0.95,step=0.01,value=0.75)
  interact(solucionD,humanos=widH, infectados=widI, zombies=widZ, muertos=fixed(0), a=wida, b=widb, z=widz, r=widr, c=widc);

def graficaComparacion():
  fig1, ax = plt.subplots(4,1, figsize=(15,20))
  
  tiempo = np.linspace(0, 10, 1000)
  humanos = 100
  infectados = 0
  zombies = 1
  muertos = 0
  cuarentena = 0
  a = 0.05
  b = 0.3
  z = 0.2
  r = 0.3
  k = 0.5
  s = 0.01
  g = 0.1
  c = 0.85
  
  estadoA = np.array([humanos, zombies,muertos])
  solA = odeint(derivadasA,estadoA, tiempo, args=(a, b, z))
  ax[0].plot(tiempo,solA.T[0], c='b', label="Humanos", linewidth=2)
  ax[0].plot(tiempo,solA.T[1], c='g', label="Zombies", linewidth=2)
  ax[0].plot(tiempo,solA.T[2], c='r', label="Muertos")
  limA = np.amax(solA)
  ax[0].set_xlabel(u"Tiempo (semanas)")
  ax[0].set_title("Modelo basico", fontweight='bold')
  ax[0].legend()
  ax[0].set_ylim(0,limA+10)
  
  estadoB = np.array([humanos,infectados,zombies,muertos])
  solB = odeint(derivadasB, estadoB, tiempo, args=(a, b, z, r))
  ax[1].plot(tiempo,solB.T[0], c='b', label="Humanos", linewidth=2)
  ax[1].plot(tiempo,solB.T[2], c='g', label="Zombies", linewidth=2)
  ax[1].plot(tiempo,solB.T[1], c='purple', label="Infectados")
  ax[1].plot(tiempo,solB.T[3], c='r', label="Muertos")
  limB = np.amax(solB)
  ax[1].set_xlabel(u"Tiempo (semanas)")
  ax[1].set_title("Modelo con infeccion latente", fontweight='bold')
  ax[1].legend()
  ax[1].set_ylim(0,limB+10)

  estadoC = np.array([humanos,infectados,zombies,muertos,cuarentena])
  solC = odeint(derivadasC, estadoC, tiempo, args=(a, b, z, r, k, s, g))
  ax[2].plot(tiempo,solC.T[0], c='b', label="Humanos", linewidth=2)
  ax[2].plot(tiempo,solC.T[2], c='g', label="Zombies", linewidth=2)
  ax[2].plot(tiempo,solC.T[1], c='purple', label="Infectados")
  ax[2].plot(tiempo,solC.T[3], c='r', label="Muertos")
  ax[2].plot(tiempo,solC.T[4], c='c', label="Cuarentena")
  limC = np.amax(solC)
  ax[2].set_xlabel(u"Tiempo (semanas)")
  ax[2].set_title(u"Modelo con cuarentena", fontweight='bold')
  ax[2].legend()
  ax[2].set_ylim(0,limC+10)
  
  estadoD = np.array([humanos,infectados,zombies,muertos])
  solD = odeint(derivadasD, estadoD, tiempo, args=(a, b, z, r, c))
  ax[3].plot(tiempo,solD.T[0], c='b', label="Humanos", linewidth=2)
  ax[3].plot(tiempo,solD.T[2], c='g', label="Zombies", linewidth=2)
  ax[3].plot(tiempo,solD.T[1], c='purple', label="Infectados")
  ax[3].plot(tiempo,solD.T[3], c='r', label="Muertos")
  limD = np.amax(solD)
  ax[3].set_xlabel(u"Tiempo (semanas)")
  ax[3].set_title(u"Modelo con tratamiento", fontweight='bold')
  ax[3].legend();
  ax[3].set_ylim(0,limD+10);
