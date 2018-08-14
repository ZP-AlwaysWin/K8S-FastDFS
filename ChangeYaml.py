#encoding=utf-8
import json
import os           
import shutil
import math
import re
from ..k8s.rbd import have_disk as have_disk
from ..k8s.rbd import get_size_need as get_size_need

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

    #*************新增检验配置文件是否为合法JSON代码**********#
    try:
        config = json.loads(read_file(config_name))
    except:
        return 1

    hosts = []
    group_num=config['GROUP_NUM']
    node_hosts = config['node_hosts']
    storage_num=config['STORAGE_NUM']
    tracker_num=config['TRACKER_SERVER_NUM']
    fastdfs_data=config['FASTDFS_DATA']
    nginx_ip=config['Nginx_Ip']

    for i in range(len(node_hosts)) :
        if node_hosts[i] not in hosts:
            hosts.append(node_hosts[i])

    return [group_num,hosts,storage_num,tracker_num,fastdfs_data,nginx_ip]

def change_tracker_yaml():

    tracker_hosts=[]

    list_config = get_config(basedir+'/'+'FastDFS.json')

    node_hosts=list_config[1]
    fastdfs_data = list_config[4]

    #给node打storage的table
    label_nodes = ""
    for i in range(len(node_hosts)):
        label_nodes += '/root/local/bin/kubectl label node {} fastdfs=storage{} >/dev/null 2>&1\n'.format(node_hosts[i],i)

    #给node打tracker的table
    for i in range(len(node_hosts)):
        label_nodes += '/root/local/bin/kubectl label node {} fastdfs-tracker=tracker >/dev/null 2>&1\n'.format(node_hosts[i])
        tracker_hosts.append(node_hosts[i])
        if i==1:
            break


    tracker_shell=read_file(basedir+'/shell/install_tracker.sh')

    tracker_shell = tracker_shell.replace("&{FASTDFS_NODES_LABEL}", label_nodes)

    write_file(basedir+"/out/shell/install_tracker.sh", tracker_shell)

    #替换FastDFS Tracker节点的YAML文件
    tracker_stateful=read_file(basedir+"/Yaml/fastdfs-tracker-statefulset.yaml")
    tracker_stateful = tracker_stateful.replace("&{FastDFS_Data}", str(fastdfs_data))

    write_file(basedir + "/out/tracker/fastdfs-tracker-statefulset.yaml", tracker_stateful)

    return [tracker_hosts]

def change_storage_yaml():
    list_config = get_config(basedir+'/'+'FastDFS.json')
    group_num=list_config[0]
    node_num = len(list_config[1])
    storage_num=list_config[2]
    fastdfs_data=list_config[4]

    list_tracker_config=change_tracker_yaml()
    tracker_hosts=list_tracker_config[0]

    label=0
    for i in range(group_num):
        for j in range(storage_num):
            storage_stateful = read_file(basedir+"/Yaml/fastdfs-storage-statefulset.yaml")

            storage_stateful = storage_stateful.replace('&{fastdfs-storage}',"fastdfs-group{}-storage{}".format(i,j))
            storage_stateful = storage_stateful.replace('&{moons}', "storage{}".format(label))
            storage_stateful = storage_stateful.replace('&{GROUP_NAME}', '\"' + "group{}".format(i) + '\"')
            storage_stateful = storage_stateful.replace('&{PORT}', '\"' + "2300{}".format(i) + '\"')
            storage_stateful = storage_stateful.replace('&{PROBE_PORT}', "2308{}".format(i))
            storage_stateful = storage_stateful.replace('&{STORAGE_NGINX_PORT}','\"'+"2308{}".format(i)+'\"')
            if len(tracker_hosts)==1:
                storage_stateful = storage_stateful.replace('&{TRACKER_NUM}'," ")
                storage_stateful = storage_stateful.replace('&{TRACKER_SERVER}', '\"'+tracker_hosts[0]+":"+"22133"+'\"' )
                storage_stateful = storage_stateful.replace('&{TRACKER_SERVER_SLAVE}'," ")
            else:
                storage_stateful = storage_stateful.replace('&{TRACKER_NUM}', '\"'+"2"+'\"')
                storage_stateful = storage_stateful.replace('&{TRACKER_SERVER}', '\"'+tracker_hosts[0]+":"+"22133"+'\"' )
                storage_stateful = storage_stateful.replace('&{TRACKER_SERVER_SLAVE}', '\"'+tracker_hosts[1]+":"+"22133"+'\"' )
            storage_stateful = storage_stateful.replace('&{FastDFS_Data}',str(fastdfs_data))
            label=label+1
            if(label==node_num):
                label=0
            write_file(basedir+"/out/storage/fastdfs-group{}-storage{}-statefulset.yaml".format(i,j), storage_stateful)

def change_nginx_yaml():
    nginx_stateful = read_file(basedir+'/Yaml/nginx-statefulset.yaml')
    list_config = get_config(basedir + '/' + 'FastDFS.json')
    node_num = len(list_config[1])
    nginx_nodes = ""

    for i in range(node_num):
        if i==0:
            nginx_nodes += '- name: K8S_NODE0{}_IP\n          value: {}\n'.format(i, list_config[1][i])
            continue
        if i+1==node_num:
            nginx_nodes += '        - name: K8S_NODE0{}_IP\n          value: {}'.format(i,list_config[1][i])
            continue
        nginx_nodes += '        - name: K8S_NODE0{}_IP\n          value: {}\n'.format(i, list_config[1][i])
    nginx_stateful = nginx_stateful.replace('&{K8S_NODE_IP}', nginx_nodes)


    write_file(basedir+'/out/nginx/nginx_stateful.yaml', nginx_stateful)

def check_config():
    # *************新增检验配置文件是否为合法JSON代码**********#
    list_config = get_config(basedir + '/' + 'FastDFS.json')
    if isinstance(list_config, int):
        print("Error!The configuration file that users fill is not the standard JSON format.")
        return 1
    #return [group_num, hosts, storage_num, tracker_num, fastdfs_data, nginx_ip]
    # *******************Add Check Config************
    group_num = list_config[0]
    storage_num = list_config[2]
    hosts = list_config[1]
    tracker_num = list_config[3]
    fastdfs_data=list_config[4]
    nginx_ip=list_config[5]

    #**************增加一句检验IP是否合法的语句*************
    node_str = os.popen("/root/local/bin/kubectl get node|awk -F ' ' 'NR>1{print $1}'").read().strip()
    node_list = node_str.split("\n")

    for i in hosts:
        if i not in node_list:
            print("Error!The NodeIP that the user fills out does not exist in the K8S cluster")
            return 1

    if isinstance(fastdfs_data,int):
        if (int(fastdfs_data) <=0 or int(fastdfs_data) >100000000000):
            print("Error!The parameters of the FastDFS mounted disk that the user fills out must be an integer greater than 0")
            return 1
    else:
        print("Error!The parameters of FastDFS mounted disk that users fill out must be int type")
        return 1
    if isinstance(tracker_num,int):
       if int(tracker_num) != 2:
          print("Error! The tracker number must be 2")
          return 1
    else:
        print("Error! The tracker number must be 2")
        return 1   

    if isinstance(storage_num,int):
        if len(hosts)<2:
            print("Error!The node IP that the user fills in at least two")
            return 1
        elif int(storage_num) <= 0:
            print("Error!The number of storage for users to fill in FastDFS must be greater than 0")
            return 1
        elif int(storage_num) > len(hosts):
            print("Error!The number of storage that FastDFS fills out must be less than or equal to the number of node IP")
            return 1
    else:
        print("Error!The number parameter of FastDFS component Storage must be int type")
        return 1

    if isinstance(group_num, int):
        if (int(group_num) <=0 or int(group_num) >3):
            print("Error!The number of the FastDFS component groups must be 1, 2, and 3")
            return 1
        else:
            #calc_disk=int(math.ceil(int(fastdfs_data)*1.075+0.5))
            #install_disk = int(group_num) * int(storage_num) * calc_disk + 12
            
            num_temp = int(group_num) * int(storage_num)
            volumes=[{'num':num_temp,'size':fastdfs_data},{'num':4,'size':5}]
            install_disk=get_size_need(volumes)
            #print(install_disk)
            return_code = have_disk(install_disk)
            if return_code == 1:
                print("Error! Install FastDFS Cluster don't have enough disk")
                return 1
    else:
        print("Error!The number of parameters of the FastDFS component group must be the int type")
        return 1

    compile_ip = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if compile_ip.match(nginx_ip):
        pass
    else:
        return 1

    return [group_num,storage_num,hosts,fastdfs_data,nginx_ip]

def get_nginx_ip():
    list_config = get_config(basedir + '/' + 'FastDFS.json')
    if isinstance(list_config, int):
        print("Error!The configuration file that users fill is not the standard JSON format.")
        return "127.0.0.1"
    nginx_ip = list_config[5]
    compile_ip = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if compile_ip.match(nginx_ip):
        return nginx_ip
    else:
        print("Error! Nginx iP is illegal ")
        return "127.0.0.1"


def check_disk():
    list_config = check_config()
    if list_config == 1:
        return 1
    else:
        group_num = list_config[0]
        storage_num = list_config[1]
        fastdfs_data = list_config[3]
    
    num_temp = int(group_num) * int(storage_num)
    volumes=[{'num':num_temp,'size':fastdfs_data},{'num':4,'size':5}]
    install_disk=get_size_need(volumes)

    #calc_disk = int(math.ceil(int(fastdfs_data) * 1.075 + 0.5))
    #install_disk = int(group_num) * int(storage_num) * calc_disk + 24

    print("The size of the disk required to install the FastDFS cluster is：%s" %install_disk)
    return install_disk




def install_all():

    #********加一句检测集群是否已经安装过的代码*********#

    fastdfs_endpoints = os.popen("/root/local/bin/kubectl get endpoints |grep -ci fastdfs").read().strip()
    fastdfs_pvc = os.popen("/root/local/bin/kubectl get pvc|grep -ci fastdfs").read().strip()
    fastdfs_service = os.popen("/root/local/bin/kubectl get service | grep -ci fastdfs").read().strip()
    fastdfs_pod = os.popen("/root/local/bin/kubectl get pod | grep -ci fastdfs").read().strip()
    fastdfs_sts = os.popen("/root/local/bin/kubectl get sts | grep -ci fastdfs").read().strip()

    return_code = fastdfs_endpoints + fastdfs_pvc + fastdfs_service + fastdfs_pod + fastdfs_sts

    if int(return_code)!=0:
        print("Error!FastDFS cluster already exists, please do not repeat the installation")
        return 1

    list_config=check_config()
    if list_config==1:
        return 1
    else:
        group_num = list_config[0]
        storage_num = list_config[1]
        hosts = list_config[2]



    source_path=basedir+'/'+'FastDFS.json'
    destination_path=basedir+'/fdfs/FastDFS.json'
    destination_bak_path=basedir+'/json/Expand_FastDFS.json'
    shutil.copy(source_path, destination_path)
    shutil.copy(source_path, destination_bak_path)


    list_tracker_config = change_tracker_yaml()
    tracker_hosts=list_tracker_config[0]

    change_storage_yaml()
    change_nginx_yaml()


    print("The number of K8S node nodes is：%d " % len(hosts))
    print("The IP of the K8S node node is：%s " % (json.dumps(hosts)))
    print("The number of the group Group of the FastDFS is：%s " % group_num)
    print("The number of Storage under each group of Group in FastDFS is：%s " % storage_num)
    print("IP as the FastDFS Tracker node is:%s " % json.dumps(tracker_hosts))

    print("Start installing the Tracker node of the FastDFS cluster")
    cmd_tracker='sh '+basedir+'/out/shell/install_tracker.sh'
    os.system(cmd_tracker)
    print("End the Tracker node of the installation of the FastDFS cluster")

    print("Start installing the Storage node of the FastDFS cluster")
    cmd_storage='sh '+basedir+'/shell/install_storage.sh'
    os.system(cmd_storage)
    print("End the Storage node of the installation of the FastDFS cluster")

    cmd_storage = 'sh ' + basedir + '/shell/install_nginx.sh'
    print("Start installing the Nginx node of the FastDFS cluster")
    os.system(cmd_storage)
    print("End the Nginx node of the installation of the FastDFS cluster")

    return 0


if __name__=="__main__":
    #check_disk()
    return_code=install_all()
    if return_code==0:
        print("SUCCESS! Install FastDFS cluster success")
    else:
        print("Error! Install FastDFS cluster failure")
    nginx_ip=get_nginx_ip()
    print(nginx_ip)

