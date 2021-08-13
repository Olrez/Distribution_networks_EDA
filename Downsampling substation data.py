#este script usa pandas time resampling para hacer un downsampling de las mediciones de subestación
#de un muestreo cada 10 minutos a un muestreo cada 15 minutos

import pandas as pd
import csv  
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import tkinter as tk
from tkinter import filedialog
import numpy as np


plt.show(block=True)

from IPython import get_ipython
get_ipython().run_line_magic('matplotlib', 'inline')
from datetime import datetime

Timestamp = [] #columna 1 csv
Q_str = [] #columna 2 csv
P_str = [] #columna 3 csv

#importacion de variables
with open('Linda Vista_ kW _KVAr.csv', 'r') as file:
#with open('SantaBarbara_kW_kVAr.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader) #se salta encabezados
    for row in reader:
        Timestamp0 = row[0]
        # list comprehension for float conversion
        Q0, P0 = [str(value) for value in row[1:]]
        #llenado de valores n vectores
        Timestamp.append(Timestamp0)
        Q_str.append(Q0)
        P_str.append(P0)

#convierte string a float
Q = list(np.float_(Q_str))
P = list(np.float_(P_str))

date = [] #se define una variable para convertir el string de timestamp a tipo datetime

for i in range(0, len(Timestamp)): 
    date0 = datetime.strptime(Timestamp[i], '%d/%m/%Y %H:%M') #%d/%m LV
    #date0 = datetime.strptime(Timestamp[i], '%m/%d/%Y %H:%M') #%m/%d SB
    date.append(date0)

#se crea el dataframe
original_data = pd.DataFrame(index = date)

# Active Power
original_data['P'] = P
# Reactive Power
original_data['Q'] = Q

original_data.head()

#downsampling, se crean las columnas en el formato del plug in rojo
fifteen_minutely_data = pd.DataFrame()
fifteen_minutely_data['P'] = original_data.P.resample('15min').ffill()
fifteen_minutely_data['Q'] = original_data.Q.resample('15min').ffill()
fifteen_minutely_data['Hour'] = fifteen_minutely_data.index.strftime('%H:%M')
fifteen_minutely_data['Day'] = fifteen_minutely_data.index.strftime('%m/%d/%Y')

fifteen_minutely_data.head()
#eliminar primera fila que no tiene info:
fifteen_minutely_data.drop(pd.Timestamp('2019-08-01 00:00:00'), inplace = True)

#esto es un loop para exportar el resultado a csv medidante una ventana, cerrar ventana una vez guardado
root= tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()

def exportCSV ():
    global fifteen_minutely_data
    
    export_file_path = filedialog.asksaveasfilename(defaultextension='.csv')
    fifteen_minutely_data.to_csv (export_file_path, index = False, header=True)

saveAsButton_CSV = tk.Button(text='Export CSV', command=exportCSV, bg='green', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 150, window=saveAsButton_CSV)

root.mainloop()

#extrae el dia 01 de agosto para graficar y comparar visualmente
one_day_graph_10 = original_data.truncate(before='2019-08-01', after='2019-08-02')
one_day_graph_15 = fifteen_minutely_data.truncate(before='2019-08-01', after='2019-08-02')


#graficos

fig, ax = plt.subplots()

ax.xaxis.set_major_formatter(DateFormatter('%H'))
ax.plot(one_day_graph_10.index, one_day_graph_10['P'], 'g-', label = '10 min')
ax.plot(one_day_graph_15.index, one_day_graph_15['P'], 'b-', label = '15 min')
plt.title("Comparacion 01 de agosto")
plt.xlabel("Hora")
plt.ylabel("P (kW)")
plt.legend(loc='upper left')
plt.savefig("out_LV.pdf", bbox_inches='tight')
#plt.savefig("out_SB.pdf", bbox_inches='tight')

plt.show()

#plt.plot(one_day_graph_10['P'],'g*', one_day_graph_15['P'], 'ro')
#plt.show()
