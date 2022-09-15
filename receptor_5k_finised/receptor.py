# -*- coding: utf-8 -*-
"""
Created on Wed Sept 7 00:41:15 2022
--------------------------------
Finished on Friday Sept 9 2022

@authors: 
    Eva Denisse Vargas Sosa, 
    Brenda Vega Méndez, 
    Sergio Adolfo Sanoja Hernández, 
    Carlos Alejandro Castro Cervantes

Project: LoRa COmmunication 
"""
import serial 
import time 
import json
import re 
import paho.mqtt.client as mqttClient

arduino = serial.Serial(port='COM8', baudrate=115200, timeout=.1)

def carga_str(b):
    #global id_t, gps, imu, vel_llantas, porcentaje, kg_proccess, vel_tri, combustible, km, aceite, presion
    d = json.loads(b)
    for x in d:
        if x == "ID_t6":
            id_t = "ok"
            #print("dentro del diccionario")
        elif x == "GPS_t6":
            #print(x, d[x])
            gps = d[x]
        elif x == "IMU_t6":
            imu = d[x]
        elif x == "VelLlantas_t6":
            vel_llantas = d[x]
        elif x == "PerLlenado_t6":
            porcentaje = d[x]
        elif x == "KgProcesados_t6":
            kg_proccess = d[x]
        elif x == "VelTri_t6":
           vel_tri = d[x]
        elif x == "NvlCombu_t6":
            combustible = d[x]
        elif x == "Km_t6":
            km = d[x] 
        elif x == "NvlAceite_t6":
            aceite = d[x]
        elif x == "PresLlantas_t6":
            presion = d[x]
        
    #print(gps, imu, vel_llantas, porcentaje, kg_proccess, vel_tri, combustible, km, aceite, presion)
    #print(type(gps))
    return (gps, imu,vel_llantas,porcentaje,kg_proccess,vel_tri,combustible,km,aceite,presion)
        
def on_connect(client, userdata, flags, rc):
    """Función que establece la conexión
    
    """
    if rc==0:
        #print("Conectado al broker")
        global Connected
        Connected = True
    else:
        print("Falla en la conexión")
    return

def conexion(gps, imu, vel_llantas, porcentaje, kg_proccess, vel_tri, combustible, km, aceite, presion):
    Connected = False  #variable para verificar el estado de la conexión
    broker_address="192.168.0.102" #dirección del Broker se puede modificar 
    port= 1883 #puerto por defecto de MQTT
    tag1 = "/CADI/I40/GPS"  #tag, etiqueta o tópico
    tag2 = "/CADI/I40/IMU"  #tag, etiqueta o tópico
    tag3 = "/CADI/I40/Wheel_speed"  #tag, etiqueta o tópico
    tag4 = "/CADI/I40/Filled_per"  #tag, etiqueta o tópico
    tag5 = "/CADI/I40/proccess_kg"  #tag, etiqueta o tópico
    tag6 = "/CADI/I40/harvester_speed"  #tag, etiqueta o tópico
    tag7 = "/CADI/I40/fuel_lvl"  #tag, etiqueta o tópico
    tag8 = "/CADI/I40/km"  #tag, etiqueta o tópico
    tag9 = "/CADI/I40/oil_lvl"  #tag, etiqueta o tópico
    tag10 = "/CADI/I40/wheel_pressure"  #tag, etiqueta o tópico
    client = mqttClient.Client("identificador") #instanciación
    client.on_connect = on_connect #agregando la función
    client.connect(broker_address, port)
    client.loop_start() #inicia la instancia
    #print(gps, imu, vel_llantas)
    try:
        client.publish(tag1,gps,qos=2)
        client.publish(tag2,imu,qos=2)
        client.publish(tag3,vel_llantas,qos=2)
        client.publish(tag4,porcentaje,qos=2)
        client.publish(tag5,kg_proccess,qos=2)
        client.publish(tag6,vel_llantas,qos=2)
        client.publish(tag7,gps,qos=2)
        client.publish(tag8,imu,qos=2)
        client.publish(tag9,vel_llantas,qos=2)
        client.publish(tag10,vel_llantas,qos=2)
        time.sleep(7) #Ceditos a Robert SI FUNCIONA XD 
    except KeyboardInterrupt: #cuando presionas Ctrl +C
        print("Envío de datos detenido por el usuario") 
        client.disconnect()
        client.loop_stop()
        
        
while True:
    time.sleep(1)
    try:
        name_byte = arduino.readline()
        name_str = name_byte.decode()
        #print(name_str)
        name_str2 = name_str.find("Received packet")
        #print(name_str2)
        if name_str2 == 0:
            name = re.sub("Received packet '","",name_str)
            name_id = name_str.find("ID_t6")
            #print(name_id)
            if name_id == 19:
                print(name)
                gps, imu,vel_llantas,porcentaje,kg_proccess,vel_tri,combustible,km,aceite,presion = carga_str(name)
                #print(gps, imu,vel_llantas,porcentaje,kg_proccess,vel_tri,combustible,km,aceite,presion )
                conexion(gps, imu,vel_llantas,porcentaje,kg_proccess,vel_tri,combustible,km,aceite,presion)
    except Exception as error:
        print("Peto")
        print(repr(error))
    #time.sleep(20)