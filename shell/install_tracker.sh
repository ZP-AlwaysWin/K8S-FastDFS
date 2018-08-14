#!/bin/bash
basepath=$(cd `dirname $0`; pwd)


/root/local/bin/kubectl create configmap fdfs-config --from-file=${basepath}/../../fdfs/ >/dev/null 2>&1

&{FASTDFS_NODES_LABEL}

/root/local/bin/kubectl create -f ${basepath}/../../out/tracker/fastdfs-tracker-statefulset.yaml >/dev/null 2>&1
sleep 20

/root/local/bin/kubectl create -f ${basepath}/../../Yaml/fastdfs-tracker-svc.yaml >/dev/null 2>&1
sleep 5

rm -rf ${basepath}/../../out/tracker/*
rm -rf ${basepath}/../../out/shell/*

