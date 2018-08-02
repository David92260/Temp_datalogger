# coding: utf-8
#!/usr/bin/python
#==========================================
# Fichier de test David Monchaux
# 31 juillet 2018
#==========================================
# Lecture d'un fichier CSV
#==========================================

import matplotlib.pyplot as plt
import numpy as np
import os
import time
import datetime

os.chdir(r'C:\NoSave\[NoSave] Documents\09_DIVERS\DSI\ELEA\Python\Test DATALOGGER')

def isConvertibleToFloat(value):
  try:
    float(value)
    return True
  except:
    return False

def isConvertibleToTime(value):
  try:
    time.strptime(value, '%d/%m/%Y %H:%M:%S')
    return True
  except:
    return False

def convertToTime(value):
  return datetime.datetime(*time.strptime(value, '%d/%m/%Y %H:%M:%S')[:6])

vecFloatConvertible = np.vectorize(isConvertibleToFloat)
vecTimeConvertible = np.vectorize(isConvertibleToTime)
vecConvertToTime = np.vectorize(convertToTime)

def createArrayFromCSV(source, tableau):
    """Créer un numpy array à partir d'un fichier CSV"""
    with open(source, 'r') as fichier:
        tableau_brut = np.array([[0,0]])
        while 1:
            ligne = fichier.readline()
            if ligne == "":
                break
            else:
                valeur = ligne[-6:-1]
                timestamp = ligne.rsplit('\t', 1)[0]
                #timestamp = time.strptime(timestamp, '%d/%m/%Y %H:%M:%S')
 
            tableau_brut = np.append(tableau_brut, [[timestamp,valeur]], axis=0)

    fichier.closed
    print tableau_brut
    mask0 = vecTimeConvertible(tableau_brut[:,0])
    tableau_1 = tableau_brut[mask0,:]    
    mask1 = vecFloatConvertible(tableau_1[:,1])
    tableau_2 = tableau_1[mask1,:]
    
    #tableau =tableau_brut[mask1,1].astype(float)
    #timestamps = tableau_brut[mask0,0]
        #print timestamps
    # tableau = np.reshape(tableau, (-1, 3, 6))
    return tableau_2

#time.strptime('20/12/2014 15:41:14', '%d/%m/%Y %H:%M:%S') => permet de créer un struct_time

if __name__ == '__main__' :
    data = np.array([])
    result = createArrayFromCSV(r'DONNEES-1.TXT', data)

    # plot with various axes scales
    fig, axs = plt.subplots()
    
    x = np.arange(result[:,0].size)
    dates = result[:,0]
    y = result[:,1]
    
    plt.xticks(rotation=70)
    axs.minorticks_on()
    axs.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    axs.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.grid(True, 'both')

    plt.ylim([21, 30])
    axs.set_autoscaley_on(False)
    axs.set_ylabel(u'Degrés Celsius')
    axs.set_title(u'Température dans le séjour')
    axs.plot(x, y)
    
    locs, labels = plt.xticks()
    plt.xticks(locs[:-1])
    labels[0]=dates[locs[0]]
    labels[1]=dates[locs[1]]    
    labels[2]=dates[locs[2]]
    labels[3]=dates[locs[3]]
    labels[4]=dates[locs[4]]
    labels[5]=dates[locs[5]]
    
    axs.set_xticklabels(labels)
        
    plt.show()

    
