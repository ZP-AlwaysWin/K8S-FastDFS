#encoding=utf-8

import os
import json
#from ..k8s.volumes import delete_volumes as delete_volumes

basedir=os.path.split(os.path.realpath(__file__))[0]

def read_file (filename):
    f = open(filename)
    content = f.read()
    f.close()
    return content

def write_file (filename, text):
    f = open(filename, 'w')
    f.write(text)
    f.close()

def get_config(config_name):
    # *************新增检验配置文件是否为合法JSON代码**********#
    try:
        config = json.loads(read_file(config_name))
    except:
        return 1
    hosts = []
    node_hosts = config['node_hosts']

    for i in range(len(node_hosts)) :
        if node_hosts[i] not in hosts:
            hosts.append(node_hosts[i])

    return hosts

def change_del():

    list_config = get_config(basedir + '/' + 'FastDFS.json')
    if isinstance(list_config, int):
        return 1

    label_nodes = ""
    for i in range(len(list_config)):
        label_nodes += '/root/local/bin/kubectl label node {} fastdfs- >/dev/null 2>&1\n'.format(list_config[i],i)
        label_nodes += '/root/local/bin/kubectl label node {} fastdfs-tracker- >/dev/null 2>&1\n'.format(list_config[i], i)

    delete_shell = read_file(basedir + '/shell/delete_fastdfs.sh')

    delete_shell = delete_shell.replace("&{del_clu_ip}", label_nodes)

    write_file(basedir + "/out/shell/delete_fastdfs.sh", delete_shell)
    return 0

def delAll():

    # ********加一句检测集群是否已经删除的代码*********#

    fastdfs_endpoints = os.popen("/root/local/bin/kubectl get endpoints |grep -ci fastdfs").read().strip()
    fastdfs_pvc = os.popen("/root/local/bin/kubectl get pvc|grep -ci fastdfs").read().strip()
    fastdfs_service = os.popen("/root/local/bin/kubectl get service | grep -ci fastdfs").read().strip()
    fastdfs_pod = os.popen("/root/local/bin/kubectl get pod | grep -ci fastdfs").read().strip()
    fastdfs_sts = os.popen("/root/local/bin/kubectl get sts | grep -ci fastdfs").read().strip()

    return_code=fastdfs_endpoints+fastdfs_pvc+fastdfs_service+fastdfs_pod+fastdfs_sts

    if int(return_code) == 0:
        print("Error!FastDFS cluster does not exist, please do not repeat the deletion")
        return 1

    del_code=change_del()
    if int(del_code)==0:
        print("Start deleting the FastDFS cluster")
        #args = os.popen("for i in `/root/local/bin/kubectl get pvc|awk '/fastdfs/{print $3}'`;do /root/local/bin/kubectl get pv -o=jsonpath='{.spec.glusterfs.path}' $i; echo "";done").read().strip()
        #pvclist = args.split("\n")

        #code = raw_input("Please input you need to delete FastDFS disk data? 1: don't delete FastDFS disk data 0: delete FastDFS disk data\n")
        code=0
        cmd_delete_fastdfs= 'sh ' + basedir + '/out/shell/delete_fastdfs.sh'
        #os.system(cmd_delete_fastdfs)
        if isinstance(code,int):
            if code==0:
                print("Start deleting the FastDFS cluster,delete FastDFS disk data")
                return_code=os.system(cmd_delete_fastdfs)
                #if return_code==0:
                #    delete_volumes(pvclist)
            elif code==1:
                os.system(cmd_delete_fastdfs)
                print("Start deleting the FastDFS cluster,don't delete FastDFS disk data")
            else:
                print("Error!The input parameter is not 0 or 1")
                return 1
        else:
            print("Error!The input parameter is not the int type")
            return 1

        print("Delete the end of the FastDFS cluster")
        return 0
    else:
        print("Delete the cluster read configuration file is not the standard JSON, please change")
        return 1

if __name__=="__main__":
    delAll()
