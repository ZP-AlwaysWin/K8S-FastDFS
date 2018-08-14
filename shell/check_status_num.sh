#!/bin/bash

basepath=$(cd `dirname $0`; pwd)

config_tracker=$1
config_storage_group=$2


/root/local/bin/kubectl get pod -o wide > /tmp/tmp_num.txt

now_storage_group=`cat /tmp/tmp_num.txt |grep -E "fastdfs-group.*Running"|wc -l`
now_tracker=`cat /tmp/tmp_num.txt|grep -E "fastdfs-tracker.*Running"|wc -l`
now_nginx=`cat /tmp/tmp_num.txt|grep -E "fastdfs-nginx-.*Running"|wc -l`

if [ ${now_tracker} -eq ${config_tracker} ] ; then
    echo "Success,The number of active Tracker Pod is consistent"
else
    echo "Error,The number of active Tracker Pod inconsistencies"
    exit 1
fi

if [ ${now_storage_group} -eq ${config_storage_group} ] ; then
    echo "Success,The number of active Group+Storage Pod is consistent"
else
    echo "Error,The number of active Group+Storage Pod inconsistencies"
    exit 1
fi

if [ ${now_nginx} -eq 2 ] ; then
    echo "Success,The number of active Nginx Pod is consistent"
else
    echo "Error,The number of active Nginx Pod inconsistencies"
    exit 1
fi
