#encoding=utf-8
import json
import os
import shutil
import math
import ChangeYaml as ym
import check_fastdfs as cf
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
    # *************新增检验配置文件是否为合法JSON代码**********#
    try:
        config = json.loads(read_file(config_name))
    except:
        return 1

    hosts = []
    group_num = config['GROUP_NUM']
    node_hosts = config['node_hosts']
    storage_num = config['STORAGE_NUM']
    tracker_num = config['TRACKER_SERVER_NUM']
    fastdfs_data = config['FASTDFS_DATA']

    for i in range(len(node_hosts)):
        if node_hosts[i] not in hosts:
            hosts.append(node_hosts[i])

    return [group_num, hosts, storage_num, tracker_num, fastdfs_data]


def check_expand_config():

    list_expand_config = get_config(basedir + '/json/Expand_FastDFS.json')
    if isinstance(list_expand_config, int):
        print("Error!The expand configuration file that users fill is not the standard JSON format.")
        return 1

    list_config = get_config(basedir + '/' + 'FastDFS.json')

    expand_group_num = list_expand_config[0]
    hosts = list_expand_config[1]
    tracker_num = list_expand_config[3]
    expand_fastdfs_data = list_expand_config[4]

    now_group_num = list_config[0]
    storage_num = list_config[2]
    now_tracker_num = list_config[3]

    if isinstance(tracker_num,int):
       if int(tracker_num) != 2:
          print("Error! The tracker number must be 2")
          return 1
    else:
        print("Error! The tracker number must be 2")
        return 1 

    if isinstance(now_tracker_num,int):
       if int(tracker_num) != 2:
          print("Error! The tracker number must be 2")
          return 1
    else:
        print("Error! The tracker number must be 2")
        return 1


    if isinstance(expand_fastdfs_data,int):
        if (int(expand_fastdfs_data) <=0 or int(expand_fastdfs_data) >10000000000):
            print("The parameters of the FastDFS mounted disk that the user fills out must be an integer greater than 0")
            return 1
    else:
        print("Error!The parameters of FastDFS mounted disk that users fill out must be int type")
        return 1

    if isinstance(expand_group_num, int):
        if (int(expand_group_num) <= 0 or int(expand_group_num) > 3):
            print("Error!The number of the FastDFS component groups must be 1, 2, and 3")
            return 1
        elif int(expand_group_num) <= int(now_group_num):
            print("Error!FastDFS components want to expand group must be larger than the number of existing groups")
            return 1
        else:
            expand_num = int(expand_group_num) - int(now_group_num)
            #calc_disk = int(math.ceil(int(expand_fastdfs_data) * 1.075 + 0.5))
            #install_disk = int(expand_num) * int(storage_num) * calc_disk

            num_temp = int(expand_num) * int(storage_num)
            volumes=[{'num':num_temp,'size':expand_fastdfs_data}]
	    
            install_disk=get_size_need(volumes)
            #print(install_disk)
            return_code=have_disk(install_disk)
            
            if return_code==1:
                print("Error! Expand Group don't have enough disk")
                return 1
    else:
        print("Error!The number of parameters of the FastDFS component group must be the int type")
        return 1
    now_hosts_list = ym.change_tracker_yaml()
    tracker_hosts = now_hosts_list[0]

    return [tracker_hosts,expand_group_num,now_group_num,storage_num,expand_fastdfs_data,hosts]

def change_storage_yaml():

    expand_config_list=check_expand_config()
    if expand_config_list==1:
        return 1
    else:
        tracker_hosts = expand_config_list[0]
        expand_group_num = expand_config_list[1]
        now_group_num = expand_config_list[2]
        storage_num = expand_config_list[3]
        expand_fastdfs_data = expand_config_list[4]
        hosts = expand_config_list[5]
        node_num=len(hosts)
    label = 0
    for i in xrange(now_group_num,expand_group_num):
        for j in range(storage_num):
            storage_stateful = read_file(basedir+"/Yaml/fastdfs-storage-statefulset.yaml")

            storage_stateful = storage_stateful.replace('&{fastdfs-storage}',"fastdfs-group{}-storage{}".format(i,j) )
            storage_stateful = storage_stateful.replace('&{moons}', "storage{}".format(label))
            storage_stateful = storage_stateful.replace('&{GROUP_NAME}', '\"' + "group{}".format(i) + '\"')
            storage_stateful = storage_stateful.replace('&{PORT}', '\"' + "2300{}".format(i) + '\"')
            storage_stateful = storage_stateful.replace('&{STORAGE_NGINX_PORT}', '\"' + "2308{}".format(i) + '\"')
            storage_stateful = storage_stateful.replace('&{PROBE_PORT}', "2308{}".format(i))
            if len(tracker_hosts)==1:
                storage_stateful = storage_stateful.replace('&{TRACKER_NUM}'," ")
                storage_stateful = storage_stateful.replace('&{TRACKER_SERVER}', '\"'+tracker_hosts[0]+":"+"22133"+'\"' )
                storage_stateful = storage_stateful.replace('&{TRACKER_SERVER_SLAVE}'," ")
            else:
                storage_stateful = storage_stateful.replace('&{TRACKER_NUM}', '\"'+"2"+'\"')
                storage_stateful = storage_stateful.replace('&{TRACKER_SERVER}', '\"'+tracker_hosts[0]+":"+"22133"+'\"' )
                storage_stateful = storage_stateful.replace('&{TRACKER_SERVER_SLAVE}', '\"'+tracker_hosts[1]+":"+"22133"+'\"' )
            storage_stateful = storage_stateful.replace('&{FastDFS_Data}', str(expand_fastdfs_data))
            label = label + 1
            if (label == node_num):
                label = 0

            write_file(basedir+"/out/storage/fastdfs-group{}-storage{}-statefulset.yaml".format(i,j), storage_stateful)
    return 0

def expand_node():
    check_code = cf.check_expand()
    if check_code != 0:
        print("Error!FastDFS cluster is not installed or clustered state exception. No expansion node is allowed！")
        return 1
    return_code = change_storage_yaml()
    if return_code==1:
        return 1

    source_path = basedir + '/json/Expand_FastDFS.json'
    destination_path = basedir + '/fdfs/FastDFS.json'
    destination_expend_path=basedir+'/FastDFS.json'

    shutil.copy(source_path, destination_path)
    shutil.copy(source_path, destination_expend_path)

    list_config = get_config(basedir+'/json/Expand_FastDFS.json')
    group_num=list_config[0]

    print("The number of the group Group of the extended FastDFS is：%s " % group_num)


    print("Start extending the Group+Storage node of the FastDFS cluster")
    cmd_storage='sh '+basedir+'/shell/expand_storage.sh'
    os.system(cmd_storage)
    print("Extending the end of the Group+Storage node of the FastDFS cluster")


if __name__=="__main__":
    expand_node()

