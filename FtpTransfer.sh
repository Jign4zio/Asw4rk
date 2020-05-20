#!/bin/bash

lftp -u $2,$3 $1 <<EOF

cd /srv/ftp/
put $4 -o $5
bye
EOF
