#!/bin/bash


dos2unix /etc/fdfs/* >/dev/null 2>&1
dos2unix /fdfs/fdfs_config/* >/dev/null 2>&1

if [ ! -f "/fdfs/fdfs_config/Expand_FastDFS.json" ]; then
    CONFIG_TRACKER_SERVER_NUM=`cat /fdfs/fdfs_config/FastDFS.json|grep TRACKER_SERVER_NUM |awk -F ":|," '{print $2}'`
    CONFIG_GROUP_NUM=`cat /fdfs/fdfs_config/FastDFS.json|grep GROUP_NUM |awk -F ":|," '{print $2}'`
    CONFIG_STORAGE_NUM=`cat /fdfs/fdfs_config/FastDFS.json|grep STORAGE_NUM|awk -F ":|," '{print $2}'`
else
    CONFIG_TRACKER_SERVER_NUM=`cat /fdfs/fdfs_config/Expand_FastDFS.json|grep TRACKER_SERVER_NUM |awk -F ":|," '{print $2}'`
    CONFIG_GROUP_NUM=`cat /fdfs/fdfs_config/Expand_FastDFS.json|grep GROUP_NUM |awk -F ":|," '{print $2}'`
    CONFIG_STORAGE_NUM=`cat /fdfs/fdfs_config/Expand_FastDFS.json|grep STORAGE_NUM|awk -F ":|," '{print $2}'`
fi



/usr/bin/fdfs_monitor /etc/fdfs/client.conf 2>/dev/null > /tmp/tmp.txt

NOW_TRACKER_SERVER_NUM=`cat /tmp/tmp.txt |grep server_count|awk -F '=|,' '{print $2}'`
NOW_GROUP_NUM=`cat /tmp/tmp.txt |grep "group count:"|awk -F ":" '{print $2}'`


tmp_num=`cat /tmp/tmp.txt |grep "active server count"|awk -F '=' '{print $2}'|uniq|wc -l`

active_num=`cat /tmp/tmp.txt |grep -c "ip_addr ="`
active_sync_num=`cat /tmp/tmp.txt |grep -Ec "ACTIVE|WAIT_SYNC"`

if [ ${tmp_num} -eq 1 ] ; then
    NOW_STORAGE_NUM=`cat /tmp/tmp.txt |grep "active server count"|awk -F '=' '{print $2}'|uniq`
fi

if [ ${CONFIG_TRACKER_SERVER_NUM} -eq ${NOW_TRACKER_SERVER_NUM} ] ; then
    echo "success,The number of active Tracker nodes is consistent"
else
    echo "error,The number of active Tracker nodes is inconsistent"
    exit 1
fi

if [ ${CONFIG_GROUP_NUM} -eq ${NOW_GROUP_NUM} ] ; then
    echo "success,The number of active Group nodes is consistent"
else
    echo "error,The number of active Group nodes is inconsistent"
    exit 1
fi


if [ ${tmp_num} -eq 1 ] && [ ${CONFIG_STORAGE_NUM} -eq ${NOW_STORAGE_NUM} ]; then
    echo "success,The number of Storage for each group corresponding to the Active is consistent"
elif [ ${active_num} -eq ${active_sync_num} ] ; then
	echo "success,The number of Active+WAIT_SYNC corresponding to each group is consistent with that of Storage."
	echo "Success, The entire FastDFS cluster detection is available and deployed successfully"
	rm -rf /tmp/tmp.txt
	exit 0
else
    echo "error,The number of Active corresponding to each group is inconsistent with that of Storage"
    exit 1
fi

echo "Success, The entire FastDFS cluster detection is available and deployed successfully"

rm -rf /tmp/tmp.txt



