#encoding=utf-8
import json
import os
import shutil
import ChangeYaml as ym

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
    config = json.loads(read_file(config_name))

    group_num=config['GROUP_NUM']
    node_hosts = config['node_hosts']
    storage_num=config['STORAGE_NUM']
    tracker_num=config['TRACKER_SERVER_NUM']
    fastdfs_data = config['FASTDFS_DATA']

    return [group_num,node_hosts,storage_num,tracker_num,fastdfs_data]

def check_expand_config():

    list_expand_config = get_config(basedir + '/json/Expand_FastDFS.json')
    list_config = get_config(basedir + '/' + 'FastDFS.json')

    expand_group_num = list_expand_config[0]
    expand_fastdfs_data = list_expand_config[4]

    now_group_num = list_config[0]
    storage_num = list_config[2]

    if isinstance(expand_fastdfs_data,int):
        if (int(expand_fastdfs_data) <=0 or int(expand_fastdfs_data) >5):
            print("用户填写的FastDFS挂载磁盘的参数必须为大于0，不大于5的整数")
            return 1
    else:
        print("用户填写的FastDFS挂载磁盘的参数必须为int类型")
        return 1

    if isinstance(expand_group_num, int):
        if (int(expand_group_num) <= 0 or int(expand_group_num) > 3):
            print("FastDFS组件组的个数必须1、2、3个")
            return 1
        elif int(expand_group_num) <= int(now_group_num):
            print("FastDFS组件想要扩充组必须大于现有组的个数")
            return 1
    else:
        print("FastDFS组件组的个数参数必须为int类型")
        return 1
    now_hosts_list = ym.change_tracker_yaml()
    tracker_hosts = now_hosts_list[0]

    return [tracker_hosts,expand_group_num,now_group_num,storage_num,expand_fastdfs_data]

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

    for i in xrange(now_group_num,expand_group_num):
        for j in range(storage_num):
            storage_stateful = read_file(basedir+"/Yaml/fastdfs-storage-statefulset.yaml")

            storage_stateful = storage_stateful.replace('&{fastdfs-storage}',"fastdfs-group{}-storage{}".format(i,j) )
            storage_stateful = storage_stateful.replace('&{moons}', "storage{}".format(j))
            storage_stateful = storage_stateful.replace('&{GROUP_NAME}', '\"' + "group{}".format(i) + '\"')
            storage_stateful = storage_stateful.replace('&{PORT}', '\"' + "2300{}".format(i) + '\"')
            storage_stateful = storage_stateful.replace('&{STORAGE_NGINX_PORT}', '\"' + "2308{}".format(i) + '\"')
            if len(tracker_hosts)==1:
                storage_stateful = storage_stateful.replace('&{TRACKER_NUM}'," ")
                storage_stateful = storage_stateful.replace('&{TRACKER_SERVER}', '\"'+tracker_hosts[0]+":"+"22133"+'\"' )
                storage_stateful = storage_stateful.replace('&{TRACKER_SERVER_SLAVE}'," ")
            else:
                storage_stateful = storage_stateful.replace('&{TRACKER_NUM}', '\"'+"2"+'\"')
                storage_stateful = storage_stateful.replace('&{TRACKER_SERVER}', '\"'+tracker_hosts[0]+":"+"22133"+'\"' )
                storage_stateful = storage_stateful.replace('&{TRACKER_SERVER_SLAVE}', '\"'+tracker_hosts[1]+":"+"22133"+'\"' )
            storage_stateful = storage_stateful.replace('&{FastDFS_Data}', str(expand_fastdfs_data))

            write_file(basedir+"/out/storage/fastdfs-group{}-storage{}-statefulset.yaml".format(i,j), storage_stateful)
    return 0

def expand_node():
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

    print("扩充后的FastDFS的组Group的个数是：%s " % group_num)


    print("开始扩充FastDFS集群的Group+Storage节点")
    cmd_storage='sh '+basedir+'/shell/expand_storage.sh'
    os.system(cmd_storage)
    print("扩充FastDFS集群的Group+Storage节点结束")


if __name__=="__main__":
    expand_node()

