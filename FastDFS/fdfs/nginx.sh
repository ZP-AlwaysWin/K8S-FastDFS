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

# 判断Tracker_Nginx PORT端口是否改变
if [ -n "$TRACKER_NGINX_PORT" ] ; then
sed -i "s|^.*listen       .*;|        listen       ${TRACKER_NGINX_PORT};|g" /tmp/fdfs_config/tracker_nginx.conf
fi


# tracker-nginx.conf中的group组的服务设置
if [ -n "$K8S_NODE01_IP" ] && [ -n "$GROUP01_STORAGE_NGINX_PORT" ] ; then

sed -i "/fdfs_group0 {/aserver ${K8S_NODE01_IP}:${GROUP01_STORAGE_NGINX_PORT} weight=1 max_fails=2 fail_timeout=30s;" /tmp/fdfs_config/tracker_nginx.conf
sed -i "/fdfs_group0 {/aserver ${K8S_NODE02_IP}:${GROUP01_STORAGE_NGINX_PORT} weight=1 max_fails=2 fail_timeout=30s;" /tmp/fdfs_config/tracker_nginx.conf
sed -i "/fdfs_group0 {/aserver ${K8S_NODE03_IP}:${GROUP01_STORAGE_NGINX_PORT} weight=1 max_fails=2 fail_timeout=30s;" /tmp/fdfs_config/tracker_nginx.conf

fi

if [ -n "$K8S_NODE02_IP" ] && [ -n "$GROUP02_STORAGE_NGINX_PORT" ] ; then

sed -i "/fdfs_group1 {/aserver ${K8S_NODE01_IP}:${GROUP02_STORAGE_NGINX_PORT} weight=1 max_fails=2 fail_timeout=30s;" /tmp/fdfs_config/tracker_nginx.conf
sed -i "/fdfs_group1 {/aserver ${K8S_NODE02_IP}:${GROUP02_STORAGE_NGINX_PORT} weight=1 max_fails=2 fail_timeout=30s;" /tmp/fdfs_config/tracker_nginx.conf
sed -i "/fdfs_group1 {/aserver ${K8S_NODE03_IP}:${GROUP02_STORAGE_NGINX_PORT} weight=1 max_fails=2 fail_timeout=30s;" /tmp/fdfs_config/tracker_nginx.conf

fi

if [ -n "$K8S_NODE03_IP" ] && [ -n "$GROUP03_STORAGE_NGINX_PORT" ] ; then

sed -i "/fdfs_group2 {/aserver ${K8S_NODE01_IP}:${GROUP03_STORAGE_NGINX_PORT} weight=1 max_fails=2 fail_timeout=30s;" /tmp/fdfs_config/tracker_nginx.conf
sed -i "/fdfs_group2 {/aserver ${K8S_NODE02_IP}:${GROUP03_STORAGE_NGINX_PORT} weight=1 max_fails=2 fail_timeout=30s;" /tmp/fdfs_config/tracker_nginx.conf
sed -i "/fdfs_group2 {/aserver ${K8S_NODE03_IP}:${GROUP03_STORAGE_NGINX_PORT} weight=1 max_fails=2 fail_timeout=30s;" /tmp/fdfs_config/tracker_nginx.conf

fi


mv /nginx/conf/nginx.conf /nginx/conf/nginx.conf_tracker
cp /tmp/fdfs_config/tracker_nginx.conf /nginx/conf/nginx.conf

/nginx/sbin/nginx -c /nginx/conf/nginx.conf >/dev/null 2>&1

if [ $? -eq 0 ] ; then
        echo "start tracker nginx success"
    else
	    echo "start tracker nginx failure"
fi


tail -f /nginx/logs/access.log



