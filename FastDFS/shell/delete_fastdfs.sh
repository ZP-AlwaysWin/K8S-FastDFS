#!/bin/bash

basepath=$(cd `dirname $0`; pwd)

/root/local/bin/kubectl get sts|grep fastdfs |awk '{print $1}' >tmp.txt
/root/local/bin/kubectl delete sts nginx
/root/local/bin/kubectl delete svc fastdfs-tracker
/root/local/bin/kubectl delete configmap fdfs-config

for i in `cat tmp.txt`
do
	/root/local/bin/kubectl delete sts $i
done

/root/local/bin/kubectl get pvc|grep fastdfs|awk '{print $1}' >tmp.txt

for i in `cat tmp.txt`
do
        /root/local/bin/kubectl delete pvc $i
done

&{del_clu_ip}

rm -rf ${basepath}/../../out/shell/*
rm -rf tmp.txt
