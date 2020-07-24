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


#Analisis Log HANA
f=open(RutaBackups+"/"+"backup_"+SIDDB+"_"+NombreCliente+".log","r")
dia = time.strftime("%d")
mes = time.strftime("%b")
date=time.strftime("%d%m")
year = time.strftime("%Y")
diccionario = {}
cache = ''
Errortype=""


for line in reversed(f.readlines()):
        #print hoy
        if "BACKUP   SAVE DATA finished successfully" in line:
                #mensaje += line
                status = "successful"
                fecha = line[0:10]+" "+line[11:19]
                print (line)
                break
        if "ERROR   BACKUP" in line:
                status = "error"
                fecha = line[0:10]+" "+line[11:19]
                Errortype = line
                print (line)
                break

#2020-05-18T19:02:57-04:00  P010125      172156a8556 INFO    BACKUP   SAVE DATA finished successfully
#2020-03-21T02:16:40-03:00  P005493      170fb7658fe ERROR   BACKUP   SAVE DATA finished with error: [447] backup could not be completed, [2000008] Error during asynchronous file transfer (io_getevents), rc=28: No space left on device; $fileCallback$=[W] , buffer= 0x00007f9f46e14000, offset= 165893115904, size= 0/536870912, file= "<root>/.COMPLETE_PRD_2020-03-21_0200_databackup_3_1" ((open, mode= W, access= rw-r-----, flags= DIRECT|TRUNCATE|MULTI_WRITERS|UNALIGNED_SIZE), factory= (root= "/hana/backup/bkpfull/" (access= rw-r-----, flags= AUTOCREATE_PATH|DISKFULL_ERROR, usage= DATA_BACKUP, fs= ext3, config= (async_write_submit_active=on,async_write_submit_blocks=all,async_read_submit=on,num_submit_queues=1,num_completion_queues=1,size_kernel_io_queue=512,max_parallel_io_requests=64,min_submit_batch_size=16,max_submit_batch_size=64))) {shortRetries= 0, fullRetries= 0 (0/10)}


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
        worksheet.update('J'+var1, Errortype)
