#!/bin/bash
/root/local/bin/kubectl get sts|grep fastdfs |awk '{print $1}' >tmp.txt
/root/local/bin/kubectl delete sts nginx
/root/local/bin/kubectl delete svc fastdfs-tracker
/root/local/bin/kubectl delete configmap fdfs-config

for i in `cat tmp.txt`
do
	/root/local/bin/kubectl delete sts $i
done

/root/local/bin/kubectl get pvc|grep fastdfs|awk '{print $1}' >tmp.txt

for i in `cat tmp.txt`
do
        /root/local/bin/kubectl delete pvc $i
done

/root/local/bin/kubectl label node 172.20.0.95 fastdfs- >/dev/null 2>&1
/root/local/bin/kubectl label node 172.20.0.95 fastdfs-tracker- >/dev/null 2>&1
/root/local/bin/kubectl label node 172.20.0.95 fastdfs-nginx- >/dev/null 2>&1
/root/local/bin/kubectl label node 172.20.0.97 fastdfs- >/dev/null 2>&1
/root/local/bin/kubectl label node 172.20.0.97 fastdfs-tracker- >/dev/null 2>&1
/root/local/bin/kubectl label node 172.20.0.97 fastdfs-nginx- >/dev/null 2>&1



rm -rf tmp.txt
