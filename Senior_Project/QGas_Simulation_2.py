
# coding: utf-8

# In[1]:

import numpy as np
import scipy 
import scipy.signal
import random
import numpy.fft
import matplotlib.pyplot as plt
exp = np.exp
arange = np.arange
from TwoD_QGas_2 import *
import sys


# In[2]:

T_i=input('Initial Temperature: ')
T_f=input('Final Temperature: ')
N_Temps=input('N Temperatures: ')
N=input('Iterations: ')
max_vel_temp=input('Max Velocity Temp: ')
tau=input('tau: ')
Interaction=input('Interaction: ')
Movement=input('Movement: ')
Decoherence_type=input('Decoherence type: ')
gas_shape_y=input('gas y length: ')
gas_shape_x=input('gas x length: ')
Seeded_Bell_States=input('Seed Bell States: ')
N_Seeded_Bell_States=input('Number of Seeded Bell States: ')
File_Name=input('File Name: ')

g,T,E,CV,M,Chi,ED=Temperature_Iteration(T_i, T_f, N_Temps, N, max_vel_temp, tau, Interaction, Movement=Movement, Decoherence_type=Decoherence_type, gas_shape=[int(gas_shape_y),int(gas_shape_x)], Temperature=T_i, Seed_Bell_States=Seeded_Bell_States, Number_Seeded_Bell_States=N_Seeded_Bell_States)

np.savetxt(File_Name,(T,E,CV,M,Chi,ED))


# In[ ]:



