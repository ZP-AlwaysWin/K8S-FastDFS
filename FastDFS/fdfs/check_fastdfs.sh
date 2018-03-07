#!/bin/bash

dos2unix /etc/fdfs/* >/dev/null 2>&1
dos2unix /tmp/fdfs_config/* >/dev/null 2>&1

if [ ! -f "/tmp/fdfs_config/Expand_FastDFS.json" ]; then
    CONFIG_TRACKER_SERVER_NUM=`cat /tmp/fdfs_config/FastDFS.json|grep TRACKER_SERVER_NUM |awk -F ":|," '{print $2}'`
    CONFIG_GROUP_NUM=`cat /tmp/fdfs_config/FastDFS.json|grep GROUP_NUM |awk -F ":|," '{print $2}'`
    CONFIG_STORAGE_NUM=`cat /tmp/fdfs_config/FastDFS.json|grep STORAGE_NUM|awk -F ":|," '{print $2}'`
else
    CONFIG_TRACKER_SERVER_NUM=`cat /tmp/fdfs_config/Expand_FastDFS.json|grep TRACKER_SERVER_NUM |awk -F ":|," '{print $2}'`
    CONFIG_GROUP_NUM=`cat /tmp/fdfs_config/Expand_FastDFS.json|grep GROUP_NUM |awk -F ":|," '{print $2}'`
    CONFIG_STORAGE_NUM=`cat /tmp/fdfs_config/Expand_FastDFS.json|grep STORAGE_NUM|awk -F ":|," '{print $2}'`
fi



/usr/bin/fdfs_monitor /etc/fdfs/client.conf > /tmp/tmp.txt

NOW_TRACKER_SERVER_NUM=`cat /tmp/tmp.txt |grep server_count|awk -F '=|,' '{print $2}'`
NOW_GROUP_NUM=`cat /tmp/tmp.txt |grep "group count:"|awk -F ":" '{print $2}'`


tmp_num=`cat /tmp/tmp.txt |grep "active server count"|awk -F '=' '{print $2}'|uniq|wc -l`


if [ ${tmp_num} -eq 1 ] ; then
    NOW_STORAGE_NUM=`cat /tmp/tmp.txt |grep "active server count"|awk -F '=' '{print $2}'|uniq`
else
    echo "error,每个组对应的Active的Storage的数量不一致"
    exit 1
fi

if [ ${CONFIG_TRACKER_SERVER_NUM} -eq ${NOW_TRACKER_SERVER_NUM} ] ; then
    echo "success,活跃的Tracker节点数量一致"
else
    echo "error,活跃的Tracker节点数量不一致"
    exit 1
fi

if [ ${CONFIG_GROUP_NUM} -eq ${NOW_GROUP_NUM} ] ; then
    echo "success,活跃的Group节点数量一致"
else
    echo "error,活跃的Group节点数量不一致"
    exit 1
fi

if [ ${CONFIG_STORAGE_NUM} -eq ${NOW_STORAGE_NUM} ] ; then
    echo "success,每个组对应的Active的Storage的数量一致"
else
    echo "error,每个组对应的Active的Storage的数量不一致"
    exit 1
fi




echo "整个FastDFS集群检测可用，部署成功"

rm -rf /tmp/tmp.txt
