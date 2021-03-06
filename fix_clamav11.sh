#! /bin/bash
dt=`date +20%y%m%d`
ti=`date +%H%M%d`
hs=`hostname`

zypper install clamav
zypper install clamsap
touch /var/log/freshclam.log
chmod 600 /var/log/freshclam.log
freshclam
clamscan ~
ps -ef | grep clam
service clamd start
service clamd enable

cp /etc/clamd.conf /etc/clamd.conf.$dt$ti
sed -i 's/3310/44410/' /etc/clamd.conf

cp ./fix_clamscan.txt /root/clamscan.sh
chmod +x /root/clamscan.sh
service clamd stop
service clamd start
echo "Revisar si el puerto 3310 esta tomado por clamd"
netstat -napt | grep 3310
echo "Validar que arriba no haya un puerto tomado por clamd"
echo "Use comando crontab -e"
echo "Luego agregue 5 0 * * * /root/clamscan.sh"
echo verifique con comando crontab -l
