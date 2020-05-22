#Copie y pegue para servidor FTP linux
#!/bin/bash

lftp -u $2,$3 $1 <<EOF

cd /srv/ftp/
put $4 -o $5
bye
EOF

#Copie y pegue para servidor FTP windows
#!/bin/bash

ftp -n -i $1 <<EOF
user $2 $3
put $4 $5
quit
EOF
