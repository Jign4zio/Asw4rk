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

#Analisis Log SyBase
f=open(os.getcwd()+"/Logs/"+SIDDB+"_"+NombreCliente+".txt","r")
dia = time.strftime("%d")
mes = time.strftime("%b")
date=time.strftime("%d%m")
diccionario = {}
cache = ''

for line in reversed(f.readlines()):
    if "DUMP is complete (database USD)." in line:
        fecha = line.rstrip()[0:20]
    if "Database USD: Verification reported" in line and cache in line:
        status=line.rstrip()[84:92]
        f.close()
        break

print fecha
print status
print fecha[0:7]
print mes

#Apertura hoja
sh = gc.open('Respaldos Diarios-'+mes)
worksheet = sh.worksheet(date)

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
        worksheet.update('I'+var1, status)
        worksheet.update('H'+var1, fecha)
