#!/bin/bash

basepath=$(cd `dirname $0`; pwd)

config_tracker=$1
config_storage_group=$2


/root/local/bin/kubectl get pod -o wide > /tmp/tmp_num.txt

now_storage_group=`cat /tmp/tmp_num.txt |grep -E "fastdfs-group.*Running"|wc -l`
now_tracker=`cat /tmp/tmp_num.txt|grep -E "fastdfs-tracker.*Running"|wc -l`
now_nginx=`cat /tmp/tmp_num.txt|grep -E "nginx-.*Running"|wc -l`

if [ ${now_tracker} -eq ${config_tracker} ] ; then
    echo "Success,活跃的Tracker Pod数量一致"
else
    echo "Error,活跃的Tracker Pod数量不一致"
    exit 1
fi

if [ ${now_storage_group} -eq ${config_storage_group} ] ; then
    echo "Success,活跃的Group+Storage Pod数量一致"
else
    echo "Error,活跃的Group+Storage Pod数量不一致"
    exit 1
fi

if [ ${now_nginx} -eq 1 ] ; then
    echo "Success,活跃的Nginx Pod数量一致"
else
    echo "Error,活跃的Nginx Pod数量不一致"
    exit 1
fi
