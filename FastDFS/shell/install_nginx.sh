#!/bin/bash
basepath=$(cd `dirname $0`; pwd)


filelist=`ls ${basepath}/../out/nginx/` >/dev/null 2>&1
for file in $filelist
do
 echo "Nginx的YMAL文件名称是：" $file
 /root/local/bin/kubectl create -f ${basepath}/../out/nginx/${file}
done
rm -rf ${basepath}/../out/nginx/*

