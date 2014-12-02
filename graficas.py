import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def derivadasA(estado, t, a, b, z):
  dh = -b*estado[0]*estado[1]
  dz = b*estado[0]*estado[1] + z*estado[2] - a*estado[0]*estado[1]
  dm = a*estado[0]*estado[1] - z*estado[2]
  return np.array([dh, dz, dm])

def graficaSolucionA(humanos, zombies, muertos, a, b, z):
  tiempo = np.linspace(0, 1, 100)
  estadoA = np.array([humanos, zombies,muertos])
  sol = odeint(derivadasA,estadoA, tiempo, args=(a, b, z))
  plt.figure(figsize=(15,5))
  plt.plot(tiempo,sol.T[0], c='b', label="Humanos")
  plt.plot(tiempo,sol.T[1], c='g', label="Zombies")
  plt.plot(tiempo,sol.T[2], c='r', label="Muertos")
  lim = np.amax(sol)
  plt.xlabel("Tiempo (semanas)")
  plt.legend()
  plt.ylim(0,lim+10)
