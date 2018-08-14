#!/bin/bash
basepath=$(cd `dirname $0`; pwd)


filelist=`ls ${basepath}/../out/nginx/` >/dev/null 2>&1
for file in $filelist
do
 if [ $file = "ReadME.txt" ];then
        continue
 fi
 echo "The YMAL file name of Nginx is：" $file
 /root/local/bin/kubectl create -f ${basepath}/../out/nginx/${file}
done
rm -rf ${basepath}/../out/nginx/*

