# -*- coding: utf-8 -*-
"""
Created on Sun May 31 22:18:36 2020

@author: Olde
"""

#import csv
import pandas as pd
#import numpy as np
circuit='LNV'
sim='LV'

P = pd.read_csv(circuit+'/INPUT/P-real-AMIS.csv',skipinitialspace=True)
P = P.set_index('intante')
P = P.fillna(0)
Q = pd.read_csv(circuit+'/INPUT/Q-real-AMIS.csv',skipinitialspace=True)
Q = Q.set_index('intante')
Q = Q.fillna(0)

amiNames = P.columns
Q_measured = Q.columns
#Q_zero = pd.DataFrame(0, index=np.arange(96), columns=['kVAr'])

fileW = open(circuit+'/OUTPUT/'+circuit+'_LoadShapesAMI.dss',"w")
for i in amiNames:
    if Q_measured.isin([str(i)]).sum() == 0:
        P[str(i)].to_csv(circuit+'/OUTPUT/AMI_P/'+str(i)+'.csv', index = False, header = False)
        #Q_zero.to_csv(circuit+'/OUTPUT/AMI_Q/'+str(i)+'.csv', index = False, header = False)
        txto = 'New Loadshape.'+str(i)+ ' npts=96 minterval=15 mult=(file=D:\\Documents\\Tesis\\Desarrollo\\Simulaciones\\'+sim+'\\AMI\\DSS\\profiles\\AMI_P\\' + i + '.csv) useactual=no'
        fileW.write(txto+'\n')
    else:
        P[str(i)].to_csv(circuit+'/OUTPUT/AMI_P/'+str(i)+'.csv', index = False, header = False)
        Q[str(i)].to_csv(circuit+'/OUTPUT/AMI_Q/'+str(i)+'.csv', index = False, header = False)
        txto = 'New Loadshape.'+str(i)+ ' npts=96 minterval=15 mult=(file=D:\\Documents\\Tesis\\Desarrollo\\Simulaciones\\'+sim+'\\AMI\\DSS\\profiles\\AMI_P\\' + i + '.csv) Qmult=(file=D:\\Documents\\Tesis\\Desarrollo\\Simulaciones\\'+sim+'\\AMI\\DSS\\profiles\\AMI_Q\\' + i + '.csv) useactual=no'
        fileW.write(txto+'\n')
fileW.close()
    
