#!/bin/bash
#set -e

# 现有环境变量
# FASTDFS_PATH=/opt/fdfs 
# FASTDFS_BASE_PATH=/var/fdfs 
# PORT= 
# GROUP_NAME= 
# TRACKER_SERVER=

# 新增的环境变量
# TRACKER_NUM=
# STORAGE_NGINX_PORT=
# TRACKER_SERVER_SLAVE=
# GROUP_NUM=


# 替换单机tracker_server的函数
function change_signle_tracker()  
{  
    if [ -n "$TRACKER_SERVER" ] ; then  

    sed -i "s|tracker_server=.*$|tracker_server=${TRACKER_SERVER}|g" /etc/fdfs/storage.conf
    sed -i "s|tracker_server=.*$|tracker_server=${TRACKER_SERVER}|g" /etc/fdfs/client.conf
    sed -i "s|tracker_server=.*$|tracker_server=${TRACKER_SERVER}|g" /etc/fdfs/mod_fastdfs.conf

    fi
}  

# 替换集群tracker_server的函数
function change_ha_tracker()  
{  
    if [ -n "$TRACKER_SERVER" ] && [ -n "$TRACKER_SERVER_SLAVE" ] ; then  

    sed -i "s|tracker_server=.*$|tracker_server=${TRACKER_SERVER}|g" /etc/fdfs/storage.conf
    sed -i "/tracker_server=.*$/atracker_server=${TRACKER_SERVER_SLAVE}" /etc/fdfs/storage.conf
    sed -i "s|tracker_server=.*$|tracker_server=${TRACKER_SERVER}|g" /etc/fdfs/client.conf
    sed -i "/tracker_server=.*$/atracker_server=${TRACKER_SERVER_SLAVE}" /etc/fdfs/client.conf
    sed -i "s|tracker_server=.*$|tracker_server=${TRACKER_SERVER}|g" /etc/fdfs/mod_fastdfs.conf
    sed -i "/tracker_server=.*$/atracker_server=${TRACKER_SERVER_SLAVE}" /etc/fdfs/mod_fastdfs.conf

    fi
}


# 创建Storage节点的data文件夹的软链接函数
function make_storage_data_link()
{
    ln -s /var/fdfs/data/ /var/fdfs/data/M00 >/dev/null 2>&1
    flag=$?
    while [ $flag -eq 0 ]
    
    do
        ln -s /var/fdfs/data/ /var/fdfs/data/M00 >/dev/null 2>&1
        flag=$?
    done

    if [ $flag -eq 1 ] ; then
        echo "make link storage data success!"
    fi

}

#启动Storage节点的nginx服务器的函数
function start_storage_nginx()
{
    /usr/local/nginx/sbin/nginx -c /etc/fdfs/nginx.conf >/dev/null 2>&1

    if [ $? -eq 0 ] ; then
        echo "start storage nginx success"
    else
	    echo "start storage nginx failure"
    fi
}


#把FDFS配置文件的configmap的挂载目录更新到容器的配置文件
rm -rf /etc/fdfs/*
cp /tmp/fdfs_config/* /etc/fdfs/

# 根据$1参数，判断是启动tracker、storage还是单纯的查看监控情况
if [ "$1" = "monitor" ] ; then
  if [ -n "$TRACKER_SERVER" ] && [ -n "$TRACKER_SERVER_SLAVE" ] ; then
    sed -i "s|tracker_server=.*$|tracker_server=${TRACKER_SERVER}|g" /etc/fdfs/client.conf
    sed -i "/tracker_server=.*$/atracker_server=${TRACKER_SERVER_SLAVE}" /etc/fdfs/client.conf
  else
    sed -i "s|tracker_server=.*$|tracker_server=${TRACKER_SERVER}|g" /etc/fdfs/client.conf
  fi
  fdfs_monitor /etc/fdfs/client.conf
  exit 0
elif [ "$1" = "storage" ] ; then
  FASTDFS_MODE="storage"
else 
  FASTDFS_MODE="tracker"
fi

# 判断PORT端口是否改变
if [ -n "$PORT" ] ; then  
sed -i "s|^port=.*$|port=${PORT}|g" /etc/fdfs/"$FASTDFS_MODE".conf
sed -i "s|storage_server_port=.*$|storage_server_port=${PORT}|g" /etc/fdfs/mod_fastdfs.conf
fi

# 判断Storage_Nginx PORT端口是否改变
if [ -n "$STORAGE_NGINX_PORT" ] ; then
sed -i "s|^.*listen       .*;|        listen       $STORAGE_NGINX_PORT;|g" /etc/fdfs/nginx.conf
fi

# 判断组名
if [ -n "$GROUP_NAME" ] ; then  
sed -i "s|group_name=.*$|group_name=${GROUP_NAME}|g" /etc/fdfs/storage.conf
sed -i "s|group_name=.*$|group_name=${GROUP_NAME}|g" /etc/fdfs/mod_fastdfs.conf
sed -i "/#flag/a[$GROUP_NAME]" /etc/fdfs/mod_fastdfs.conf
fi 

# 替换mod_fastdfs.conf组的个数
if [ -n "$GROUP_NUM" ]; then
sed -i "s|group_count =.*$|group_count = ${GROUP_NUM}|g" /etc/fdfs/mod_fastdfs.conf
fi

#根据组的个数，判断是否启动单个tracker(不填写TRACKER_NUM的值)；还是高可用tracker(填写TRACKER_NUM为2)
if [ -n "$TRACKER_NUM" ] ; then
    change_ha_tracker
else
    change_signle_tracker
fi

FASTDFS_LOG_FILE="${FASTDFS_BASE_PATH}/logs/${FASTDFS_MODE}d.log"
PID_NUMBER="${FASTDFS_BASE_PATH}/data/fdfs_${FASTDFS_MODE}d.pid"

echo "try to start the $FASTDFS_MODE node..."
if [ -f "$FASTDFS_LOG_FILE" ]; then 
	rm "$FASTDFS_LOG_FILE"
fi
# start the fastdfs node.	
fdfs_${FASTDFS_MODE}d /etc/fdfs/${FASTDFS_MODE}.conf start

# wait for pid file(important!),the max start time is 5 seconds,if the pid number does not appear in 5 seconds,start failed.
TIMES=60
while [ ! -f "$PID_NUMBER" -a $TIMES -gt 0 ]
do
    sleep 1s
	TIMES=`expr $TIMES - 1`
done

# if the storage node start successfully, print the started time.
if [ $TIMES -gt 0  ]; then
    
	if [ "$1" = "storage" ]; then
        echo "the ${FASTDFS_MODE} node started successfully at $(date +%Y-%m-%d_%H:%M)"
        make_storage_data_link
        start_storage_nginx
    else
        echo "the ${FASTDFS_MODE} node started successfully at $(date +%Y-%m-%d_%H:%M)"
    fi
	# give the detail log address
    echo "please have a look at the log detail at $FASTDFS_LOG_FILE"

    # leave balnk lines to differ from next log.
    echo
    echo

	# make the container have foreground process(primary commond!)
    tail -f "$FASTDFS_LOG_FILE"
# else print the error.
else
    echo "the ${FASTDFS_MODE} node started failed at $(date +%Y-%m-%d_%H:%M)"
	echo "please have a look at the log detail at $FASTDFS_LOG_FILE"
	echo
    echo
    tail -f "$FASTDFS_LOG_FILE"
fi
tail -f "$FASTDFS_LOG_FILE"

