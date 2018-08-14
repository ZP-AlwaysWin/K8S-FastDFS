#!/bin/bash
count=0
while true ; do
        for i in `kubectl get pod |awk '/fastdfs/{print $1}'`;
        do
                kubectl delete pod $i
        done
        while true; do
                sleep 10
                code=`python -m scripts.fastdfs.check_fastdfs|tail -1`
                if [ $code -eq 0 ];then
                        break
                fi
        done
        let count+=1
        echo $count > success.log
done