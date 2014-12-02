%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

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
