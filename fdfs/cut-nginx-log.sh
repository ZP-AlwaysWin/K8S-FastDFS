#!/bin/bash  
  
LOGS_PATH=/var/log/nginx  
YESTERDAY=$(date +%Y-%m-%d-%H) 
mv ${LOGS_PATH}/access.log ${LOGS_PATH}/access_${YESTERDAY}.log  
mv ${LOGS_PATH}/error.log ${LOGS_PATH}/error_${YESTERDAY}.log  


kill -USR1 $(cat /var/run/nginx.pid)  

find /var/log/nginx -mtime +7 -name "*.log" | xargs rm -f
