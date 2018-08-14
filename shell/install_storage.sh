#!/bin/bash
basepath=$(cd `dirname $0`; pwd)

fast_yaml=0
filelist=`ls $basepath/../out/storage` >/dev/null 2>&1

for file in $filelist
do
 if [ $file = "ReadME.txt" ];then
        continue
 fi
 let fast_yaml+=1;
 echo "The YMAL file name of Storage is：" $file
 /root/local/bin/kubectl create -f ${basepath}/../out/storage/${file}
 sleep 1
done

makestorage(){

 for file in $filelist
 do
  if [ $file = "ReadME.txt" ];then
         continue
  fi
  /root/local/bin/kubectl create -f ${basepath}/../out/storage/${file} >/dev/null 2>&1
  sleep 1
 done

}
now_storage_sts=`/root/local/bin/kubectl get sts|grep -ic fastdfs-group`

while [ $fast_yaml -ne $now_storage_sts ]; do
    makestorage
	now_storage_sts=`/root/local/bin/kubectl get sts|grep -ic fastdfs-group`
done

rm -rf ${basepath}/../out/storage/*