#! /bin/bash

ps -ef|grep fdfs |grep -v grep >/tmp/probe-s_tmp.txt

cat>/tmp/probe-s_config.txt<<EOF
/bin/bash /fdfs/fdfs_config/start.sh storage
fdfs_storaged /etc/fdfs/storage.conf start
nginx: master process /usr/local/nginx/sbin/nginx -c /etc/fdfs/nginx.conf
tail -f --follow=name /var/fdfs/logs/storaged.log
EOF


for i in `seq 1 4`;do
        head=`sed -n "${i}p" /tmp/probe-s_config.txt`

        if [ `grep -c "${head}" /tmp/probe-s_tmp.txt` -eq '1' ]; then
                continue
        else
                exit 1
        fi
done

