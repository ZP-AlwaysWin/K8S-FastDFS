#encoding=utf-8

import os
import json

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
    node_hosts = config['node_hosts']

    for i in range(len(node_hosts)) :
        if node_hosts[i] not in hosts:
            hosts.append(node_hosts[i])

    return hosts

def change_del():

    list_config = get_config(basedir + '/' + 'FastDFS.json')
    label_nodes = ""
    for i in range(len(list_config)):
        label_nodes += '/root/local/bin/kubectl label node {} fastdfs- >/dev/null 2>&1\n'.format(list_config[i],i)
        label_nodes += '/root/local/bin/kubectl label node {} fastdfs-tracker- >/dev/null 2>&1\n'.format(list_config[i], i)
        label_nodes += '/root/local/bin/kubectl label node {} fastdfs-nginx- >/dev/null 2>&1\n'.format(list_config[i],i)

    delete_shell = read_file(basedir + '/shell/delete_fastdfs.sh')

    delete_shell = delete_shell.replace("&{del_clu_ip}", label_nodes)

    write_file(basedir + "/out/shell/delete_fastdfs.sh", delete_shell)

def delAll():
    change_del()
    print("开始删除FastDFS集群")
    cmd_delete_fastdfs= 'sh ' + basedir + '/out/shell/delete_fastdfs.sh'
    os.system(cmd_delete_fastdfs)
    print("删除FastDFS集群结束")

if __name__=="__main__":
    delAll()