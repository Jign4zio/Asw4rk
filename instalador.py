# -*- coding: utf-8 -*-
#!/usr/bin/python
import requests
import os

#Estructura de la
Horario= {'PAR':"00 01", 'MIN': "30 01", 'ADP': "00 02", 'AZA': "30 02",
'AUS': "00 03", 'MUT': "30 03", 'CPT': "03 01", 'CBT': "33 01", 'NPH': "03 02",
'CHX': "33 02", 'UDP': "03 03", 'COL': "33 03", 'BLP': "07 01", 'UDC': "37 01", 'SAV': "03 02"}
DBorder = {'1':'ScriptSyBase.py', '2':'ScriptHANA.py', '3':'ScriptMaxDB', '4':'ScriptOracle'}

#Descarga dependencias necesarias

url = 'https://www.python.org/static/img/python-logo@2x.png'
myfile = requests.get(url)

url1 = 'https://raw.githubusercontent.com/Jign4zio/Asw4rk/master/ScriptSybase.py'
url2 = 'https://raw.githubusercontent.com/Jign4zio/Asw4rk/master/ftptransfer.sh'
url3 = 'https://raw.githubusercontent.com/Jign4zio/Asw4rk/master/ScriptHANA.py'

open('PythonImage.png', 'wb').write(myfile.content)
ScriptSyBase = requests.get(url1)
FtpTransfer = requests.get(url2)
ScriptHANA = requests.get(url3)

open('ScriptSyBase.py', 'wb').write(ScriptSyBase.content)
open('FtpTransfer.sh', 'wb').write(FtpTransfer.content)
open('ScriptHANA.py', 'wb').write(ScriptHANA.content)


#Pregunta el SID de la base de datos, nombre de cliente, tipo de SO y lo escribe en un cliente.SID.conf
print("Instalador agente monitoreo respaldos, favor indique los datos solicitados")
print("Nombre cliente (Nomenclatura planilla, Ej: MIN, PAR, CHX, CPT)")
NombreCliente = raw_input()
NombreCliente = NombreCliente.upper()
print("Ingrese el SID de la DB a monitorear")
SIDDB=raw_input()
SIDDB=SIDDB.upper()
print("Ingrese el SID del sistema al cual pertenece la DB")
SIDSAP=raw_input()
SIDSAP=SIDSAP.upper()
print("Indique si el sistema a monitorear es WIN o LNX")
SO=raw_input()
SO=SO.upper()
print("Indique si el sistema donde está ejecutando este script es WIN, o LNX")
SOAppmon=raw_input()
SOAppmon=SOAppmon.upper()
print("Marque 1 para indicar que esta monitoreando una DB SyBase, 2 para DB HANA, 3 para DB MaxDB, 4 para DB oracle")
DBType=raw_input()

#Creación scripts programables
print (" \n***ACTIVIDADES A REALIZAR EN SERVIDOR BASE DE DATOS***\n\n")


if DBType == '1':
    PathLog = "/sybase/"+SIDDB+"/ASE-16_0/install/"+SIDDB+"_BS.log"
    Output = SIDDB+"_BS_"+NombreCliente+".log"

if DBType == '2':
    MinCrontab = Horario[NombreCliente][0:2]
    print ("-Debe crear la ruta /root/BKlog\n")
    print ("-Añada la siguiente linea al crontab del servidor \n")
    print("-IMPORTANTE!: De existir una entrada de CRONTAB que se ejecute a la misma hora que la arrojada por este instalador, sumar 2min al crontab nuevo")
    MinCrontab = int(MinCrontab)-5
    print ("\n-Reemplazar HDB10 por HDB+Nro de instancia de DB\n-Reemplazar hostname_servidor por hostname de servidor\n")
    print (str(MinCrontab)+" "+Horario[NombreCliente][3:5]+" * * * /hana/shared/"+SIDDB+"/HDB10/hostname_servidor/trace/backup.log >> /root/BKlog/backup_"+SIDDB+"_"+NombreCliente+".log\n")
    PathLog = "/root/BKlog/backup_"+SIDDB+"_"+NombreCliente+".log"
    Output = "backup_"+SIDDB+"_"+NombreCliente+".log"

if SO == "WIN":
    print ("hola")

if SO == 'LNX':
    print ("Agregue la siguiente linea al crontab")
    print("\nIMPORTANTE!: De existir una entrada de CRONTAB que se ejecute a la misma hora que la arrojada por este instalador, sumar 2min al crontab nuevo\n")
    print(Horario[NombreCliente]+" * * * /root/BKmon/FtpTransfer.sh Hostname UsuarioFTP PasswordFTP "+PathLog+" "+Output)

print (" \n***ACTIVIDADES A REALIZAR EN SERVIDOR MONITOREO***\n\n")

if SOAppmon == 'WIN':
    print("copie la siguiente entrada y ejecutela en la consola de la maquina contenedora del servidor FTP")
    print("Schtasks.exe /C /MO DAILY /ST "+Horario[NombreCliente][3:5]+":"+Horario[NombreCliente][0:2]+" /TR "+os.getcwd()+"/"+DBorder[DBType]+" "+NombreCliente+" "+SIDDB+" "+SIDSAP+" "+SO)

if SOAppmon == 'LNX':
    f=open(NombreCliente+"_"+SIDDB+".sh", "wb")
    f.write("#!/bin/bash\n")
    f.write("#En caso de de querer editar la entrada del script siga la siguiente nomenclatura\n")
    f.write("#python "+os.getcwd()+"/"+DBorder[DBType]+" NombreCliente SIDBaseDeDatos SistemaOperativo SID\n")
    f.write("python "+os.getcwd()+"/"+DBorder[DBType]+" "+NombreCliente+" "+SIDDB+" "+SIDSAP+" "+SO+"\n")
    f.close()
    print("copie la siguiente entrada y asignela a crontab")
    print("IMPORTANTE!: De existir una entrada de CRONTAB que se ejecute a la misma hora que la arrojada por este instalador, sumar 2min al crontab nuevo")
    print(Horario[NombreCliente]+" * * * "+os.getcwd()+"/"+NombreCliente+"_"+SIDDB+".sh")


#https://recursospython.com/guias-y-manuales/la-linea-de-comandos-para-pythonistas/
