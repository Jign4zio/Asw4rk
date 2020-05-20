#!/bin/bash

# $1 is the file name for the you want to tranfer
# usage: this_script  <hostname> <usernameftp> <passwordftp> <filename> <output>
#IP_address="xx.xxx.xx.xx"
#username="remote_ftp_username"
#domain = sample.domain.ftp
#password= password

ftp -n > ftp_$$.log <<EOF
 verbose
 open $1
 USER $2 $3
 put $4 -o $5
 bye
EOF
