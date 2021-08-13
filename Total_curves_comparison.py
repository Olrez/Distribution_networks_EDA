# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 14:13:38 2020

@author: Olrez
Este script grafica las figuras de P y Q con la curva de alimentador, suma de trafos disponibles y suma de clientes disponibles
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

circuit = 'LV'

#lectura

info = pd.read_csv(circuit+'/info.csv') #información con porcentajes totales disponibles en medicón por tipo (trafo o cliente)
new_columns = info.columns.values
new_columns[0] = 'Type'
info.columns = new_columns
info = info.set_index('Type')

P_transf = pd.read_csv(circuit+'/P-trafos-kW-5-Agosto.csv')
P_transf = P_transf.set_index('Time') #redefine indice segun columna fecha
P_client = pd.read_csv(circuit+'/P-clientes-kW-5-Agosto.csv')
P_client = P_client.set_index('Time')

Q_transf = pd.read_csv(circuit+'/Q-trafos-kVAr-5-Agosto.csv')
Q_transf = Q_transf.set_index('Time')
Q_client = pd.read_csv(circuit+'/Q-clientes-kVAr-5-Agosto.csv')
Q_client = Q_client.set_index('Time')

feeder = pd.read_csv(circuit+'/Subestacion_kW_kVAr.csv')
feeder = feeder.set_index(P_transf.index)

#suma de curvas medidas
Total_P_transf = P_transf.sum(1) #obtiene la curva total de trafos medidos
Total_Q_transf = Q_transf.sum(1)

Total_P_client = P_client.sum(1) #obtiene la curva total de clientes medidos
Total_Q_client = Q_client.sum(1)

#graficas
x = []
for i in range(96): #definición de variable x de gráficos
    x.append(i/4)
x = pd.Series(x)

if circuit == 'LV':
    name = 'Linda Vista'
elif circuit == 'SB':
    name = 'Santa Bárbara'

f, (ax1, ax2) = plt.subplots(1, 2, figsize=(25,10))
f.suptitle('Comparación curvas de potencia mediciones CNFL, circuito '+name)

ax1.plot(x, feeder['P'], color=[1,0.5,0.1], marker = 'o')
ax1.plot(x, Total_P_transf, color=[0.1,0.5,1], marker = 'o')
ax1.plot(x, Total_P_client, color=[0.3,1,0.7], marker = 'o')
ax1.set_title('Potencia activa (P) \n Porcentaje de trafos medidos: '+str(info.loc['Transf']['P'])+'%'+'\n Porcentaje de clientes medidos: '+str(info.loc['Client']['P'])+'%')
ax1.legend(['Curva alimentador, '+str(round(feeder['P'].sum()*0.25,2))+' kWh','Suma curvas transformadores, '+str(round(Total_P_transf.sum()*0.25,2))+' kWh','Suma curvas clientes, '+str(round(Total_P_client.sum()*0.25,2))+' kWh'], loc='upper left', numpoints=1)
ax1.set_xlabel('Hora (5 de agosto 2019)')
ax1.set_ylabel('kW')
ax1.xaxis.set_major_locator(MultipleLocator(2))
ax1.grid(which='major', linestyle=':', linewidth='0.5', color='black')  
ax1.margins(x=0,y=0)

ax2.plot(x, feeder['Q'], color=[1,0.5,0.1], marker = 'o')
ax2.plot(x, Total_Q_transf, color=[0.1,0.5,1], marker = 'o')
ax2.plot(x, Total_Q_client, color=[0.1,1,0.5], marker = 'o')
ax2.set_title('Potencia reactiva (Q) \n Porcentaje de trafos medidos: '+str(info.loc['Transf']['Q'])+'%'+'\n Porcentaje de clientes medidos: '+str(info.loc['Client']['Q'])+'%')
ax2.legend(['Curva alimentador, '+str(round(feeder['Q'].sum()*0.25,2))+' kVArh','Suma curvas transformadores, '+str(round(Total_Q_transf.sum()*0.25,2))+' kVArh','Suma curvas clientes, '+str(round(Total_Q_client.sum()*0.25,2))+' kVArh'], loc='upper left', numpoints=1)
ax2.set_xlabel('Hora (5 de agosto 2019)')
ax2.set_ylabel('kVAr')
ax2.xaxis.set_major_locator(MultipleLocator(2))
ax2.grid(which='major', linestyle=':', linewidth='0.5', color='black')
ax2.margins(x=0,y=0)

f.show()
f.savefig(circuit+'/Curvas totales circuito '+name+'.png', bbox_inches='tight') #figure export
