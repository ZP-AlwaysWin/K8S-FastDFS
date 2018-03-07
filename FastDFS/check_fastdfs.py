#encoding=utf-8
import os
import ChangeYaml as yaml


basedir=os.path.split(os.path.realpath(__file__))[0]


def check_fastdfs():
    if os.path.exists(basedir + '/' + 'Expand_FastDFS.json'):
        config_list = yaml.get_config(basedir + '/' + 'Expand_FastDFS.json')
    else:
        config_list = yaml.get_config(basedir + '/' + 'FastDFS.json')

    group_num = config_list[0]
    storage_num = config_list[2]
    tracker_num = str(config_list[3])

    group_storage_num = str(storage_num * group_num)

    cmd_check_nginx_num = "sh " + basedir + "/shell/check_status_num.sh" + ' ' + tracker_num + ' ' + group_storage_num
    code_active_pod = os.system(cmd_check_nginx_num)
    if code_active_pod!=0:
        return code_active_pod
    return code_active_pod

def check_status():
    code_active_pod=check_fastdfs()

    if code_active_pod!=0:
        print("Error! FastDFS+Nginx的集群启动的Pod数量错误！")
        return code_active_pod
    else:
        print("Success! FastDFS+Nginx的集群启动的Pod数量正确！开始检测FastDFS+Nginx内部服务是否正常")

    cmd_check_fastdfs_status="/root/local/bin/kubectl exec -ti fastdfs-group0-storage0-0 sh /etc/fdfs/check_fastdfs.sh"
    cmd_check_nginx_status="/root/local/bin/kubectl exec -ti nginx-0 sh /tmp/fdfs_config/check_nginx.sh"

    code_fastdfs_status=os.system(cmd_check_fastdfs_status)
    code_nginx_status=os.system(cmd_check_nginx_status)

    if code_fastdfs_status!=0:
        print("Error! Fastdfs集群内部服务错误" )
        return code_fastdfs_status
    if code_nginx_status!=0:
        print("Error! Nginx集群内部服务错误！")
        return code_nginx_status
    print("Success! Fastdfs&&Nginx 集群全部启动成功!")
    return 0


if __name__=="__main__":
    code=check_status()
    print(code)