#!/bin/bash
#set -e

# 环境变量列表
# TRACKER_NGINX_PORT=
# K8S_NODE01_IP=
# K8S_NODE02_IP=
# K8S_NODE03_IP=
# GROUP01_STORAGE_NGINX_PORT=
# GROUP02_STORAGE_NGINX_PORT=
# GROUP03_STORAGE_NGINX_PORT=

rm -rf /nginx/fdfs_config/
mkdir -p /nginx/fdfs_config/
cp /nginx_tmp/fdfs_config/* /nginx/fdfs_config/



# 判断Tracker_Nginx PORT端口是否改变
if [ -n "$TRACKER_NGINX_PORT" ] ; then
sed -i "s|^.*listen       .*;|        listen       ${TRACKER_NGINX_PORT};|g" /nginx/fdfs_config/tracker_nginx.conf
fi

function change_nginx0()
{
   sed -i "/fdfs_group0 {/aserver ${1}:${2} weight=1 max_fails=2 fail_timeout=30s;" /nginx/fdfs_config/tracker_nginx.conf
}

function change_nginx1()
{
   sed -i "/fdfs_group1 {/aserver ${1}:${2} weight=1 max_fails=2 fail_timeout=30s;" /nginx/fdfs_config/tracker_nginx.conf
}

function change_nginx2()
{
   sed -i "/fdfs_group2 {/aserver ${1}:${2} weight=1 max_fails=2 fail_timeout=30s;" /nginx/fdfs_config/tracker_nginx.conf
}

function change_nginx3()
{
   sed -i "/fdfs_group3 {/aserver ${1}:${2} weight=1 max_fails=2 fail_timeout=30s;" /nginx/fdfs_config/tracker_nginx.conf
}

function change_nginx4()
{
   sed -i "/fdfs_group4 {/aserver ${1}:${2} weight=1 max_fails=2 fail_timeout=30s;" /nginx/fdfs_config/tracker_nginx.conf
}

function change_nginx5()
{
   sed -i "/fdfs_group5 {/aserver ${1}:${2} weight=1 max_fails=2 fail_timeout=30s;" /nginx/fdfs_config/tracker_nginx.conf
}

function change_nginx6()
{
   sed -i "/fdfs_group6 {/aserver ${1}:${2} weight=1 max_fails=2 fail_timeout=30s;" /nginx/fdfs_config/tracker_nginx.conf
}

function change_nginx7()
{
   sed -i "/fdfs_group7 {/aserver ${1}:${2} weight=1 max_fails=2 fail_timeout=30s;" /nginx/fdfs_config/tracker_nginx.conf
}

function change_nginx8()
{
   sed -i "/fdfs_group8 {/aserver ${1}:${2} weight=1 max_fails=2 fail_timeout=30s;" /nginx/fdfs_config/tracker_nginx.conf
}

function change_nginx9()
{
   sed -i "/fdfs_group9 {/aserver ${1}:${2} weight=1 max_fails=2 fail_timeout=30s;" /nginx/fdfs_config/tracker_nginx.conf
}

# tracker-nginx.conf中的group组的服务设置

if [ -n "$K8S_NODE00_IP" ] ; then
    change_nginx0 ${K8S_NODE00_IP} ${GROUP01_STORAGE_NGINX_PORT}
    change_nginx1 ${K8S_NODE00_IP} ${GROUP02_STORAGE_NGINX_PORT}
    change_nginx2 ${K8S_NODE00_IP} ${GROUP03_STORAGE_NGINX_PORT}
    change_nginx3 ${K8S_NODE00_IP} ${GROUP04_STORAGE_NGINX_PORT}
    change_nginx4 ${K8S_NODE00_IP} ${GROUP05_STORAGE_NGINX_PORT}
    change_nginx5 ${K8S_NODE00_IP} ${GROUP06_STORAGE_NGINX_PORT}
    change_nginx6 ${K8S_NODE00_IP} ${GROUP07_STORAGE_NGINX_PORT}
    change_nginx7 ${K8S_NODE00_IP} ${GROUP08_STORAGE_NGINX_PORT}
    change_nginx8 ${K8S_NODE00_IP} ${GROUP09_STORAGE_NGINX_PORT}
    change_nginx9 ${K8S_NODE00_IP} ${GROUP010_STORAGE_NGINX_PORT}
fi

if [ -n "$K8S_NODE01_IP" ] ; then
    change_nginx0 ${K8S_NODE01_IP} ${GROUP01_STORAGE_NGINX_PORT}
    change_nginx1 ${K8S_NODE01_IP} ${GROUP02_STORAGE_NGINX_PORT}
    change_nginx2 ${K8S_NODE01_IP} ${GROUP03_STORAGE_NGINX_PORT}
    change_nginx3 ${K8S_NODE01_IP} ${GROUP04_STORAGE_NGINX_PORT}
    change_nginx4 ${K8S_NODE01_IP} ${GROUP05_STORAGE_NGINX_PORT}
    change_nginx5 ${K8S_NODE01_IP} ${GROUP06_STORAGE_NGINX_PORT}
    change_nginx6 ${K8S_NODE01_IP} ${GROUP07_STORAGE_NGINX_PORT}
    change_nginx7 ${K8S_NODE01_IP} ${GROUP08_STORAGE_NGINX_PORT}
    change_nginx8 ${K8S_NODE01_IP} ${GROUP09_STORAGE_NGINX_PORT}
    change_nginx9 ${K8S_NODE01_IP} ${GROUP010_STORAGE_NGINX_PORT}
fi

if [ -n "$K8S_NODE02_IP" ] ; then
    change_nginx0 ${K8S_NODE02_IP} ${GROUP01_STORAGE_NGINX_PORT}
    change_nginx1 ${K8S_NODE02_IP} ${GROUP02_STORAGE_NGINX_PORT}
    change_nginx2 ${K8S_NODE02_IP} ${GROUP03_STORAGE_NGINX_PORT}
    change_nginx3 ${K8S_NODE02_IP} ${GROUP04_STORAGE_NGINX_PORT}
    change_nginx4 ${K8S_NODE02_IP} ${GROUP05_STORAGE_NGINX_PORT}
    change_nginx5 ${K8S_NODE02_IP} ${GROUP06_STORAGE_NGINX_PORT}
    change_nginx6 ${K8S_NODE02_IP} ${GROUP07_STORAGE_NGINX_PORT}
    change_nginx7 ${K8S_NODE02_IP} ${GROUP08_STORAGE_NGINX_PORT}
    change_nginx8 ${K8S_NODE02_IP} ${GROUP09_STORAGE_NGINX_PORT}
    change_nginx9 ${K8S_NODE02_IP} ${GROUP010_STORAGE_NGINX_PORT}
fi

if [ -n "$K8S_NODE03_IP" ] ; then
    change_nginx0 ${K8S_NODE03_IP} ${GROUP01_STORAGE_NGINX_PORT}
    change_nginx1 ${K8S_NODE03_IP} ${GROUP02_STORAGE_NGINX_PORT}
    change_nginx2 ${K8S_NODE03_IP} ${GROUP03_STORAGE_NGINX_PORT}
    change_nginx3 ${K8S_NODE03_IP} ${GROUP04_STORAGE_NGINX_PORT}
    change_nginx4 ${K8S_NODE03_IP} ${GROUP05_STORAGE_NGINX_PORT}
    change_nginx5 ${K8S_NODE03_IP} ${GROUP06_STORAGE_NGINX_PORT}
    change_nginx6 ${K8S_NODE03_IP} ${GROUP07_STORAGE_NGINX_PORT}
    change_nginx7 ${K8S_NODE03_IP} ${GROUP08_STORAGE_NGINX_PORT}
    change_nginx8 ${K8S_NODE03_IP} ${GROUP09_STORAGE_NGINX_PORT}
    change_nginx9 ${K8S_NODE03_IP} ${GROUP010_STORAGE_NGINX_PORT}
fi

if [ -n "$K8S_NODE04_IP" ] ; then
    change_nginx0 ${K8S_NODE04_IP} ${GROUP01_STORAGE_NGINX_PORT}
    change_nginx1 ${K8S_NODE04_IP} ${GROUP02_STORAGE_NGINX_PORT}
    change_nginx2 ${K8S_NODE04_IP} ${GROUP03_STORAGE_NGINX_PORT}
    change_nginx3 ${K8S_NODE04_IP} ${GROUP04_STORAGE_NGINX_PORT}
    change_nginx4 ${K8S_NODE04_IP} ${GROUP05_STORAGE_NGINX_PORT}
    change_nginx5 ${K8S_NODE04_IP} ${GROUP06_STORAGE_NGINX_PORT}
    change_nginx6 ${K8S_NODE04_IP} ${GROUP07_STORAGE_NGINX_PORT}
    change_nginx7 ${K8S_NODE04_IP} ${GROUP08_STORAGE_NGINX_PORT}
    change_nginx8 ${K8S_NODE04_IP} ${GROUP09_STORAGE_NGINX_PORT}
    change_nginx9 ${K8S_NODE04_IP} ${GROUP010_STORAGE_NGINX_PORT}
fi

if [ -n "$K8S_NODE05_IP" ] ; then
    change_nginx0 ${K8S_NODE05_IP} ${GROUP01_STORAGE_NGINX_PORT}
    change_nginx1 ${K8S_NODE05_IP} ${GROUP02_STORAGE_NGINX_PORT}
    change_nginx2 ${K8S_NODE05_IP} ${GROUP03_STORAGE_NGINX_PORT}
    change_nginx3 ${K8S_NODE05_IP} ${GROUP04_STORAGE_NGINX_PORT}
    change_nginx4 ${K8S_NODE05_IP} ${GROUP05_STORAGE_NGINX_PORT}
    change_nginx5 ${K8S_NODE05_IP} ${GROUP06_STORAGE_NGINX_PORT}
    change_nginx6 ${K8S_NODE05_IP} ${GROUP07_STORAGE_NGINX_PORT}
    change_nginx7 ${K8S_NODE05_IP} ${GROUP08_STORAGE_NGINX_PORT}
    change_nginx8 ${K8S_NODE05_IP} ${GROUP09_STORAGE_NGINX_PORT}
    change_nginx9 ${K8S_NODE05_IP} ${GROUP010_STORAGE_NGINX_PORT}
fi

if [ -n "$K8S_NODE06_IP" ] ; then
    change_nginx0 ${K8S_NODE06_IP} ${GROUP01_STORAGE_NGINX_PORT}
    change_nginx1 ${K8S_NODE06_IP} ${GROUP02_STORAGE_NGINX_PORT}
    change_nginx2 ${K8S_NODE06_IP} ${GROUP03_STORAGE_NGINX_PORT}
    change_nginx3 ${K8S_NODE06_IP} ${GROUP04_STORAGE_NGINX_PORT}
    change_nginx4 ${K8S_NODE06_IP} ${GROUP05_STORAGE_NGINX_PORT}
    change_nginx5 ${K8S_NODE06_IP} ${GROUP06_STORAGE_NGINX_PORT}
    change_nginx6 ${K8S_NODE06_IP} ${GROUP07_STORAGE_NGINX_PORT}
    change_nginx7 ${K8S_NODE06_IP} ${GROUP08_STORAGE_NGINX_PORT}
    change_nginx8 ${K8S_NODE06_IP} ${GROUP09_STORAGE_NGINX_PORT}
    change_nginx9 ${K8S_NODE06_IP} ${GROUP010_STORAGE_NGINX_PORT}
fi

if [ -n "$K8S_NODE07_IP" ] ; then
    change_nginx0 ${K8S_NODE07_IP} ${GROUP01_STORAGE_NGINX_PORT}
    change_nginx1 ${K8S_NODE07_IP} ${GROUP02_STORAGE_NGINX_PORT}
    change_nginx2 ${K8S_NODE07_IP} ${GROUP03_STORAGE_NGINX_PORT}
    change_nginx3 ${K8S_NODE07_IP} ${GROUP04_STORAGE_NGINX_PORT}
    change_nginx4 ${K8S_NODE07_IP} ${GROUP05_STORAGE_NGINX_PORT}
    change_nginx5 ${K8S_NODE07_IP} ${GROUP06_STORAGE_NGINX_PORT}
    change_nginx6 ${K8S_NODE07_IP} ${GROUP07_STORAGE_NGINX_PORT}
    change_nginx7 ${K8S_NODE07_IP} ${GROUP08_STORAGE_NGINX_PORT}
    change_nginx8 ${K8S_NODE07_IP} ${GROUP09_STORAGE_NGINX_PORT}
    change_nginx9 ${K8S_NODE07_IP} ${GROUP010_STORAGE_NGINX_PORT}
fi

if [ -n "$K8S_NODE08_IP" ] ; then
    change_nginx0 ${K8S_NODE08_IP} ${GROUP01_STORAGE_NGINX_PORT}
    change_nginx1 ${K8S_NODE08_IP} ${GROUP02_STORAGE_NGINX_PORT}
    change_nginx2 ${K8S_NODE08_IP} ${GROUP03_STORAGE_NGINX_PORT}
    change_nginx3 ${K8S_NODE08_IP} ${GROUP04_STORAGE_NGINX_PORT}
    change_nginx4 ${K8S_NODE08_IP} ${GROUP05_STORAGE_NGINX_PORT}
    change_nginx5 ${K8S_NODE08_IP} ${GROUP06_STORAGE_NGINX_PORT}
    change_nginx6 ${K8S_NODE08_IP} ${GROUP07_STORAGE_NGINX_PORT}
    change_nginx7 ${K8S_NODE08_IP} ${GROUP08_STORAGE_NGINX_PORT}
    change_nginx8 ${K8S_NODE08_IP} ${GROUP09_STORAGE_NGINX_PORT}
    change_nginx9 ${K8S_NODE08_IP} ${GROUP010_STORAGE_NGINX_PORT}
fi

if [ -n "$K8S_NODE09_IP" ] ; then
    change_nginx0 ${K8S_NODE09_IP} ${GROUP01_STORAGE_NGINX_PORT}
    change_nginx1 ${K8S_NODE09_IP} ${GROUP02_STORAGE_NGINX_PORT}
    change_nginx2 ${K8S_NODE09_IP} ${GROUP03_STORAGE_NGINX_PORT}
    change_nginx3 ${K8S_NODE09_IP} ${GROUP04_STORAGE_NGINX_PORT}
    change_nginx4 ${K8S_NODE09_IP} ${GROUP05_STORAGE_NGINX_PORT}
    change_nginx5 ${K8S_NODE09_IP} ${GROUP06_STORAGE_NGINX_PORT}
    change_nginx6 ${K8S_NODE09_IP} ${GROUP07_STORAGE_NGINX_PORT}
    change_nginx7 ${K8S_NODE09_IP} ${GROUP08_STORAGE_NGINX_PORT}
    change_nginx8 ${K8S_NODE09_IP} ${GROUP09_STORAGE_NGINX_PORT}
    change_nginx9 ${K8S_NODE09_IP} ${GROUP010_STORAGE_NGINX_PORT}
fi

rm  /etc/nginx/nginx.conf.default
cp /nginx/fdfs_config/tracker_nginx.conf /etc/nginx/nginx.conf

/usr/sbin/nginx -c /etc/nginx/nginx.conf >/dev/null 2>&1

if [ $? -eq 0 ] ; then
        echo "start tracker nginx success"
    else
	echo "start tracker nginx failure"
fi


tail -F /var/log/nginx/access.log



