#!/bin/bash
basepath=$(cd `dirname $0`; pwd)


filelist=`ls $basepath/../out/storage` >/dev/null 2>&1
for file in $filelist
do
 echo "Storage的YMAL文件名称是：" $file
 /root/local/bin/kubectl create -f ${basepath}/../out/storage/${file}
 sleep 1
done
rm -rf ${basepath}/../out/storage/*
