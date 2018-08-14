#! /bin/bash

ps -ef|grep fdfs |grep -v grep >/tmp/probe-t_tmp.txt

cat>/tmp/probe-t_config.txt<<EOF
/bin/bash /fdfs/fdfs_config/start.sh tracker
fdfs_trackerd /etc/fdfs/tracker.conf start
tail -f --follow=name /var/fdfs/logs/trackerd.log
EOF


for i in `seq 1 3`;do
        head=`sed -n "${i}p" /tmp/probe-t_config.txt`

        if [ `grep -c "${head}" /tmp/probe-t_tmp.txt` -eq '1' ]; then
                continue
        else
                exit 1
        fi
done

