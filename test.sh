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

/root/local/bin/kubectl label node &{del_clu_ip} fastdfs-
/root/local/bin/kubectl label node &{del_clu_ip} fastdfs-
/root/local/bin/kubectl label node &{del_clu_ip} fastdfs-

/root/local/bin/kubectl label node &{del_clu_ip} fastdfs-tracker-
/root/local/bin/kubectl label node 172.20.0.96 fastdfs-tracker-
/root/local/bin/kubectl label node 172.20.0.97 fastdfs-tracker-

/root/local/bin/kubectl label node 172.20.0.95 fastdfs-nginx-
/root/local/bin/kubectl label node 172.20.0.96 fastdfs-nginx-
/root/local/bin/kubectl label node 172.20.0.97 fastdfs-nginx-


rm -rf tmp.txt
