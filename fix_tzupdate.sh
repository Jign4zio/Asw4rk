#! /bin/bash
#
# Script para actualizar modificacion cambio hora chile continental 2k19
echo
echo
echo Creando directorio Timeupdate
mkdir Timeupdate
cd Timeupdate
echo Descargan2 tzdata2k19
wget ftp://ftp.iana.org/tz/releases/tzdata2019a.tar.gz
echo
echo Descomprimiendo tzupdate en `pwd`
echo
tar xvfz tzdata2019a.tar.gz
echo
echo Timezone antiguo
echo
zdump -v Chile/Continental | grep 2019
echo
echo
echo Instalando Timezone nuevo
echo
zic southamerica
zic backward
echo
echo Timezone nuevo instalado
echo
echo Eliminando carpeta timezone
cd ..
rm -R Timeupdate
echo
echo Timezone nuevo
zdump -v Chile/Continental | grep 2019
