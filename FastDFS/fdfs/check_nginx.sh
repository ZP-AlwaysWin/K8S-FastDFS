#! /bin/bash

ps -ef|grep nginx |grep -v grep >/tmp/tmp.txt

cat>/tmp/config.txt<<EOF
/bin/bash /tmp/fdfs_config/nginx.sh
nginx: master process /nginx/sbin/nginx -c /nginx/conf/nginx.conf
tail -f /nginx/logs/access.log
nginx: worker process
nginx: cache manager process
EOF


for i in `seq 1 5`;do
        head=`sed -n "${i}p" /tmp/config.txt`

        if [ `grep -c "${head}" /tmp/tmp.txt` -eq '1' ]; then

                echo "success ${head}"
        else
                echo "error ${head}"
                exit 1
        fi
done
echo "Nginx Server is all ok"