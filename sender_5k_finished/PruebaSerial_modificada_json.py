# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 18:51:17 2022
--------------------------------
Code Finised on Friday Sept 2 
--------------------------------

@authors: 
    Eva Denisse Vargas Sosa, 
    Brenda Vega Méndez, 
    Sergio Adolfo Sanoja Hernández, 
    Carlos Alejandro Castro Cervantes

Project: LoRa COmmunication  

"""
import pandas as pd
import time
from datetime import datetime
import json
import serial

arduino = serial.Serial(port='COM3', baudrate=115200, timeout=.1)

def read_csv():

    dataframe=pd.read_csv("DatosPruebaMQTT_5k.csv",index_col=0)
    dataframe.head()
    
    dataframe.describe(include="all")
    df=dataframe.dropna() #aquí voy a limpiar todos los valores no numéricos
    
    gps = df.GPS.tolist()
    imu = df.IMU.tolist()
    vel_llantas = df.VelocidadLlantas.tolist()
    llenado = df.PorcentajeLlenado.tolist()
    procesadosk = df.KilosProcesados.tolist()
    vel_tri = df.VelocidadTrilladora.tolist()
    combustible = df.NivelCombustible.tolist()
    kilometraje = df.Kilometraje.tolist()
    aceite = df.NivelAceite.tolist()
    presion_llantas = df.PresionLlantas.tolist()

    return gps, imu, vel_llantas, llenado, procesadosk, vel_tri, combustible, kilometraje, aceite, presion_llantas

    #print("Temp", temp, "\n", "Hum",  hum, "\n",  "Co", co, "\n","Light", light,"\n", "HumidityRatio", hr )   FUNCIONA :)
      
def sender(gps, imu, vel_llantas, llenado, procesadosk, vel_tri, combustible, kilometraje, aceite, presion_llantas, d):
    for i,j,k,l,m,n,o,p,q,r in zip(gps, imu, vel_llantas, llenado, procesadosk, vel_tri, combustible, kilometraje, aceite, presion_llantas):
        for t in d: 
            if t == "GPS_t6":
                d[t]= str(i) 
                #print("entre")
            elif t == "IMU_t6":
                d[t] = str(j)
            elif t == "VelLlantas_t6":
                d[t] = str(k)
            elif t == "PerLlenado_t6":
                d[t] = str(l)
            elif t == "KgProcesados_t6":
                d[t] = str(m)
            elif t == "VelTri_t6":
                d[t] = str(n)
            elif t == "NvlCombu_t6":
                d[t] = str(o)
            elif t == "Km_t6":
                d[t] = str(p)
            elif t == "NvlAceite_t6":
                d[t] = str(q)
            elif t == "PresLlantas_t6":
                d[t] = str(r)
        a = json.dumps(d)
        b = write(a.encode('utf-8'))
            
def write(data): 
    arduino.write(bytes(data))
    time.sleep(7)
    arduino_data = arduino.readline()
    print(arduino_data)
    print(data)

while True:
    gps, imu, vel_llantas, llenado, procesadosk, vel_tri, combustible, kilometraje, aceite, presion_llantas = read_csv()
    #d = json()
    with open('sensor.json') as f:
      d= json.loads(f.read())
    sender(gps, imu, vel_llantas, llenado, procesadosk, vel_tri, combustible, kilometraje, aceite, presion_llantas, d)
    