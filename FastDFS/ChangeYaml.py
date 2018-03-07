#encoding=utf-8
import json
import os           
import shutil

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

    hosts = []
    group_num=config['GROUP_NUM']
    node_hosts = config['node_hosts']
    storage_num=config['STORAGE_NUM']
    tracker_num=config['TRACKER_SERVER_NUM']
    fastdfs_data=config['FASTDFS_DATA']

    for i in range(len(node_hosts)) :
        if node_hosts[i] not in hosts:
            hosts.append(node_hosts[i])

    return [group_num,hosts,storage_num,tracker_num,fastdfs_data]

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

    # 给node打nginx的table
    label_nodes += '/root/local/bin/kubectl label node {} fastdfs-nginx=nginx >/dev/null 2>&1\n'.format(node_hosts[-1])

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
    storage_num=list_config[2]
    fastdfs_data=list_config[4]

    list_tracker_config=change_tracker_yaml()
    tracker_hosts=list_tracker_config[0]

    for i in range(group_num):
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
            storage_stateful = storage_stateful.replace('&{FastDFS_Data}',str(fastdfs_data))

            write_file(basedir+"/out/storage/fastdfs-group{}-storage{}-statefulset.yaml".format(i,j), storage_stateful)

def change_nginx_yaml():
    nginx_stateful = read_file(basedir+'/Yaml/nginx-statefulset.yaml')
    list_tracker_config = change_tracker_yaml()
    hosts = list_tracker_config[0]

    if len(hosts)==1:
        nginx_stateful = nginx_stateful.replace('&{K8S_NODE01_IP}', '\"' + hosts[0] + '\"')
        nginx_stateful = nginx_stateful.replace('&{K8S_NODE02_IP}', '\"' + "127.0.0.1" + '\"')
        nginx_stateful = nginx_stateful.replace('&{K8S_NODE03_IP}', '\"' + "127.0.0.1" + '\"')
    elif len(hosts)==2:
        nginx_stateful = nginx_stateful.replace('&{K8S_NODE01_IP}', '\"' + hosts[0] + '\"')
        nginx_stateful = nginx_stateful.replace('&{K8S_NODE02_IP}', '\"' + hosts[1] + '\"')
        nginx_stateful = nginx_stateful.replace('&{K8S_NODE03_IP}', '\"' + "127.0.0.1" + '\"')
    else:
        nginx_stateful = nginx_stateful.replace('&{K8S_NODE01_IP}', '\"' + hosts[0] + '\"')
        nginx_stateful = nginx_stateful.replace('&{K8S_NODE02_IP}', '\"' + hosts[1] + '\"')
        nginx_stateful = nginx_stateful.replace('&{K8S_NODE03_IP}', '\"' + hosts[2] + '\"')

    write_file(basedir+'/out/nginx/nginx_stateful.yaml', nginx_stateful)

def check_config():
    # *******************Add Check Config************
    list_config = get_config(basedir + '/' + 'FastDFS.json')
    group_num = list_config[0]
    storage_num = list_config[2]
    hosts = list_config[1]
    fastdfs_data=list_config[4]

    if isinstance(fastdfs_data,int):
        if (int(fastdfs_data) <=0 or int(fastdfs_data) >5):
            print("用户填写的FastDFS挂载磁盘的参数必须为大于0，不大于5的整数")
            return 1
    else:
        print("用户填写的FastDFS挂载磁盘的参数必须为int类型")
        return 1

    if isinstance(storage_num,int):
        if len(hosts)<2:
            print("用户填写的node ip去重后至少两个")
            return 1
        elif int(storage_num) <= 0:
            print("用户填写的FastDFS 的storage的个数必须是大于0的整数")
            return 1
        elif int(storage_num) > len(hosts):
            print("用户填写的FastDFS 的storage的个数必须小于等于node ip去重后的个数")
            return 1
    else:
        print("FastDFS组件Storage的个数参数必须为int类型")
        return 1

    if isinstance(group_num, int):
        if (int(group_num) <=0 or int(group_num) >3):
            print("FastDFS组件组的个数必须1、2、3个")
            return 1
    else:
        print("FastDFS组件组的个数参数必须为int类型")
        return 1
    return [group_num,storage_num,hosts,fastdfs_data]

def get_nginx_ip():
    list_nginx = get_config(basedir + '/' + 'FastDFS.json')
    nginx_ip = list_nginx[1][-1]

    return nginx_ip

def install_all():

    list_config=check_config()
    if list_config==1:
        return 1
    else:
        group_num = list_config[0]
        storage_num = list_config[1]
        hosts = list_config[2]
        #fastdfs_data=list_config[3]



    source_path=basedir+'/'+'FastDFS.json'
    destination_path=basedir+'/fdfs/FastDFS.json'
    destination_bak_path=basedir+'/json/Expand_FastDFS.json'
    shutil.copy(source_path, destination_path)
    shutil.copy(source_path, destination_bak_path)


    list_tracker_config = change_tracker_yaml()
    tracker_hosts=list_tracker_config[0]

    change_storage_yaml()
    change_nginx_yaml()


    print("K8S node节点的数量是：%d " % len(hosts))
    print("K8S node节点的IP是：%s " % (json.dumps(hosts)))
    print("FastDFS的组Group的个数是：%s " % group_num)
    print("FastDFS的每个组Group的下的Storage个数是：%s " % storage_num)
    print("作为FastDFS Tracker节点的IP是:%s " % json.dumps(tracker_hosts))

    print("开始安装FastDFS集群的Tracker节点")
    cmd_tracker='sh '+basedir+'/out/shell/install_tracker.sh'
    os.system(cmd_tracker)
    print("安装FastDFS集群的Tracker节点结束")

    print("开始安装FastDFS集群的Storage节点")
    cmd_storage='sh '+basedir+'/shell/install_storage.sh'
    os.system(cmd_storage)
    print("安装FastDFS集群的Storage节点结束")

    cmd_storage = 'sh ' + basedir + '/shell/install_nginx.sh'
    print("开始安装FastDFS集群的Nginx节点")
    os.system(cmd_storage)
    print("安装FastDFS集群的Nginx节点结束")

    return 0


if __name__=="__main__":
    install_all()
    nginx_ip=get_nginx_ip()
    print(nginx_ip)

