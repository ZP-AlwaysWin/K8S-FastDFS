#!/bin/bash

basepath=$(cd `dirname $0`; pwd)

config_tracker=$1
config_storage_group=$2


/root/local/bin/kubectl get pod -o wide > /tmp/tmp_num.txt

now_storage_group=`cat /tmp/tmp_num.txt |grep -E "fastdfs-group.*Running"|wc -l`
now_tracker=`cat /tmp/tmp_num.txt|grep -E "fastdfs-tracker.*Running"|wc -l`
now_nginx=`cat /tmp/tmp_num.txt|grep -E "fastdfs-nginx-.*Running"|wc -l`

if [ ${now_tracker} -ne ${config_tracker} ] ; then
    exit 1
fi

if [ ${now_storage_group} -ne ${config_storage_group} ] ; then
    exit 1
fi

if [ ${now_nginx} -ne 2 ] ; then
    exit 1
fi

rm -rf /tmp/tmp_num.txt
