# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 20:10:47 2020

@author: Olde
This script extracts the august 5th data for transformers using macro info
"""

import pandas as pd
import numpy as np

circuit = 'LV'

#P-active power
dataP = pd.read_csv('P(kW)-2019-Agosto.csv') #lee archivo de 639 MB de agosto
new_columns = dataP.columns.values
new_columns[0] = 'Time'
dataP.columns = new_columns
dataP['Time'] = pd.to_datetime(dataP['Time'], format='%Y-%m-%d %H:%M:%S') #2019-08-01 00:00:00
dataP = dataP.set_index('Time')
dataP.head()
dataP = dataP.truncate(before='2019-08-05 00:00:00', after='2019-08-05 23:45:00') #extract only the simulation day

nameP = dataP.columns.astype(int) # Extract meter names
#nameP.to_csv('namesP.csv')
trafos = pd.read_csv(circuit+'/trafos.csv')

availableTP = pd.Series(np.intersect1d(nameP.values,trafos.values))

#extract transformer P data

for i in range(len(availableTP)):
    label = availableTP[i]
    P_i = dataP[str(label)]
    if i == 0:
        P_medT = P_i
    else:
        P_medT = pd.concat([P_medT, P_i], axis=1, sort=False)

P_medT.to_csv(circuit+'/P-trafos-kW-5-Agosto.csv') #export result

#extract client data
clientes = pd.read_csv(circuit+'/clientes.csv')
availableCP = pd.Series(np.intersect1d(nameP.values,clientes.values))

for i in range(len(availableCP)):
    label = availableCP[i]
    P_i = dataP[str(label)]
    if i == 0:
        P_medC = P_i
    else:
        P_medC = pd.concat([P_medC, P_i], axis=1, sort=False)

P_medC.to_csv(circuit+'/P-clientes-kW-5-Agosto.csv')


#%%
#Q-reactive power
dataQ = pd.read_csv('Q(kVAr)-2019-Agosto.csv') #lee el archivo de 198 MB de agosto
new_columns = dataQ.columns.values
new_columns[0] = 'Time'
dataQ.columns = new_columns
dataQ['Time'] = pd.to_datetime(dataQ['Time'], format='%Y-%m-%d %H:%M:%S')
dataQ = dataQ.set_index('Time')
dataQ.head()
dataQ = dataQ.truncate(before='2019-08-05 00:00:00', after='2019-08-05 23:45:00')


nameQ = dataQ.columns.astype(int)
#nameQ.to_csv('namesQ.csv')
availableTQ = pd.Series(np.intersect1d(nameQ.values,trafos.values))

#extract transformer Q data

for i in range(len(availableTQ)):
    label = availableTQ[i]
    Q_i = dataQ[str(label)]
    if i == 0:
        Q_medT = Q_i
    else:
        Q_medT = pd.concat([Q_medT, Q_i], axis=1, sort=False)

Q_medT.to_csv(circuit+'/Q-trafos-kVAr-5-Agosto.csv')

#extract client data

availableCQ = pd.Series(np.intersect1d(nameQ.values,clientes.values))

for i in range(len(availableCQ)):
    label = availableCQ[i]
    Q_i = dataQ[str(label)]
    
    if i == 0:
        Q_medC = Q_i
    else:
        Q_medC = pd.concat([Q_medC, Q_i], axis=1, sort=False)

Q_medC.to_csv(circuit+'/Q-clientes-kVAr-5-Agosto.csv')
