# -*- coding: utf-8 -*-
"""
Created on Sun May 31 12:02:30 2020

@author: Olde
This script calculate the sum of clients measurements defined by its transformer 
and plot a double PQ figure with the comparison between sum of clients and transformer
curves.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

circuit = 'SB'

P_transf = pd.read_csv(circuit+'/P-trafos-kW-5-Agosto.csv')
P_transf = P_transf.set_index('Time') #redefine indice segun columna fecha
P_client = pd.read_csv(circuit+'/P-clientes-kW-5-Agosto.csv')
P_client = P_client.set_index('Time')
P_client = P_client.fillna(0) #llena filas vacías con 0

Q_transf = pd.read_csv(circuit+'/Q-trafos-kVAr-5-Agosto.csv')
Q_transf = Q_transf.set_index('Time')
Q_client = pd.read_csv(circuit+'/Q-clientes-kVAr-5-Agosto.csv')
Q_client = Q_client.set_index('Time')
Q_client = Q_client.fillna(0)

transf_data = pd.read_csv(circuit+'/transformer_data.csv')
client_data = pd.read_csv(circuit+'/client_data.csv')
client_transf_meter = client_data.merge(transf_data,on='Group_LV') #obtine la matriz clientes pero con número de medidor de trafo según id group low voltage (medidores sin data quedan excluidos)

available_transf = pd.Series(np.intersect1d(transf_data['Meter'],P_transf.columns.astype(int))).astype(int) #transformadores medidos encontrados en el GIS

P_sum_clients = pd.DataFrame(0, index=P_transf.index, columns=available_transf.astype(str)) #matriz vacía con ids
Q_sum_clients = pd.DataFrame(0, index=Q_transf.index, columns=available_transf.astype(str))
percentage = pd.DataFrame(0, index=available_transf.astype(str), columns=['P','Q']).astype(float) #matriz vacía para porcentaje de medición de clientes por ramal de transformador medido
info = pd.DataFrame(0, index=['Transf','Client'], columns=['P','Q']).astype(float) #matriz vacía para porcentaje de medición total de circuito

def safe_div(x,y): #función para evadir error de división por cero
    try:
        return x/y
    except ZeroDivisionError:
        return 0

for i in available_transf:
    circuit_clients = client_transf_meter[client_transf_meter['Meter'] == i]['Client'] #obtiene la lista de clientes del trasformador i
    availableP = pd.Series(np.intersect1d(circuit_clients.values,P_client.columns.astype(int))) #clientes disponibles en mediciones
    percentage.loc[str(i)]['P'] = round(safe_div(availableP.size,circuit_clients.size)*100,1) #porcentaje de insersión AMI de circuito
    availableQ = pd.Series(np.intersect1d(circuit_clients.values,Q_client.columns.astype(int)))
    percentage.loc[str(i)]['Q'] = round(safe_div(availableQ.size,circuit_clients.size)*100,1)
    P_sum_clients[str(i)] = P_client[availableP.values.astype(str)].sum(1) #obtiene la suma de clientes del trafo i
    Q_sum_clients[str(i)] = Q_client[availableQ.values.astype(str)].sum(1)

P_sum_clients.to_csv(circuit+'/P-suma-clientes-kW-5-Agosto.csv')
Q_sum_clients.to_csv(circuit+'/Q-suma-clientes-kVAr-5-Agosto.csv')
percentage.to_csv(circuit+'/Porcentaje AMI.csv')

info.loc['Transf']['P'] = round(safe_div(len(P_transf.columns),len(transf_data))*100,1)
info.loc['Transf']['Q'] = round(safe_div(len(Q_transf.columns),len(transf_data))*100,1)
info.loc['Client']['P'] = round(safe_div(len(P_client.columns),len(client_data))*100,1)
info.loc['Client']['Q'] = round(safe_div(len(Q_client.columns),len(client_data))*100,1)
info.to_csv(circuit+'/info.csv')

#cálculo de info porcentajes generales

x = []
for i in range(96): #definición de variable x de gráficos
    x.append(i/4)
x = pd.Series(x)
plt.ioff()

for i in P_sum_clients.columns.astype(str): #gráficos
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(25,10))
    f.suptitle('Comparación curvas de potencia mediciones CNFL, trafo '+i)

    ax1.plot(x, P_transf[i], color=[1,0.5,0.1], marker = 'o')
    ax1.plot(x, P_sum_clients[i], color=[0.1,0.5,1], marker = 'o')
    ax1.set_title('Potencia activa (P) \n Porcentaje de clientes medidos: '+str(percentage.loc[i]['P'])+'%')
    ax1.legend(['Curva AMI trafo, '+str(np.round(P_transf[i].sum()*0.25,2))+' kWh','Suma curvas AMI clientes, '+str(np.round(P_sum_clients[i].sum()*0.25,2))+' kWh'], loc='upper right', numpoints=1)
    ax1.set_xlabel('Hora (5 de agosto 2019)')
    ax1.set_ylabel('kW')
    ax1.xaxis.set_major_locator(MultipleLocator(2))
    ax1.grid(which='major', linestyle=':', linewidth='0.5', color='black')  
    ax1.margins(x=0,y=0)

    ax2.plot(x, Q_transf[i], color=[1,0.5,0.1], marker = 'o')
    ax2.plot(x, Q_sum_clients[i], color=[0.1,0.5,1], marker = 'o')
    ax2.set_title('Potencia reactiva (Q) \n Porcentaje de clientes medidos: '+str(percentage.loc[i]['Q'])+'%') 
    ax2.legend(['Curva AMI trafo, '+str(np.round(Q_transf[i].sum()*0.25,2))+' kVArh','Suma curvas AMI clientes, '+str(np.round(Q_sum_clients[i].sum()*0.25,2))+' kVArh'], loc='upper right', numpoints=1)
    ax2.set_xlabel('Hora (5 de agosto 2019)')
    ax2.set_ylabel('kVAr')
    ax2.xaxis.set_major_locator(MultipleLocator(2))
    ax2.grid(which='major', linestyle=':', linewidth='0.5', color='black')
    ax2.margins(x=0,y=0)
    
    f.show()
    f.savefig(circuit+'/plots/'+i+'.png', bbox_inches='tight') #figure export
