# -*- coding: utf-8 -*-
#!/usr/bin/python
#Librerias requeridas
import sys
import gspread
import time
import os
#Apertura conexion Google Sheets
gc = gspread.service_account()

#Tratamiento argumentos script
NombreCliente = sys.argv[1]
SIDDB = sys.argv[2]
SIDSAP = sys.argv[3]
SO = sys.argv[4]
RutaBackups = sys.argv[5]

#Analisis Log SyBase
f=open(RutaBackups+"/"+SIDDB+"_"+NombreCliente+".log","r")
dia = time.strftime("%d")
mes = time.strftime("%b")
date= time.strftime("%d%m")
year= time.strftime("%Y")
diccionario = {}
cache = ''

control1 ="DUMP is complete (database "+SIDDB+")."
control2 = "Database "+SIDDB+": Verification reported"

for line in reversed(f.readlines()):
    if control1 in line:
        fecha = line.rstrip()[0:20]
    if control2 in line and cache in line:
        status=line.rstrip()[84:92]
        f.close()
        break

#Apertura hoja
sh = gc.open('Respaldos Diarios-'+mes+year)
worksheet = sh.worksheet(dia)

# Busqueda de celdas con NombreCliente
FindNombreCliente = worksheet.findall(NombreCliente)
ListNombreCliente = []
for cell in FindNombreCliente:
    if str(cell)[9] != "C":
        ListNombreCliente.append(str(cell)[7:10])
    else:
        ListNombreCliente.append(str(cell)[7:9])

#Busqueda de celdas con SIDDB
FindSIDDB = worksheet.findall(SIDDB)
ListSIDDB = []
for cell in FindSIDDB:
    if str(cell)[9] != "C":
        ListSIDDB.append(str(cell)[7:10])
    else:
        ListSIDDB.append(str(cell)[7:9])

#Cruce de busquedas y escritura en planilla
for var1 in ListSIDDB:
    if var1 in ListNombreCliente:
        print ("Fila afectada: "+var1)
        worksheet.update('G'+var1, status)
        worksheet.update('F'+var1, fecha)
