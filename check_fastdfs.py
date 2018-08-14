#encoding=utf-8
import os
import ChangeYaml as yaml


basedir=os.path.split(os.path.realpath(__file__))[0]

def check_expand_fastdfs():
    if os.path.exists(basedir + '/' + 'Expand_FastDFS.json'):
        config_list = yaml.get_config(basedir + '/' + 'Expand_FastDFS.json')
    else:
        config_list = yaml.get_config(basedir + '/' + 'FastDFS.json')
    
    if isinstance(config_list, int):
        print("Error!The configuration file that users fill is not the standard JSON format.")
        return 1
    
    group_num = config_list[0]
    storage_num = config_list[2]
    tracker_num = str(config_list[3])

    group_storage_num = str(storage_num * group_num)

    cmd_check_nginx_num = "sh " + basedir + "/shell/check_expand_status.sh" + ' ' + tracker_num + ' ' + group_storage_num
    code_active_pod = os.system(cmd_check_nginx_num)
    if code_active_pod != 0:
        return code_active_pod
    return code_active_pod




def check_fastdfs():
    if os.path.exists(basedir + '/' + 'Expand_FastDFS.json'):
        config_list = yaml.get_config(basedir + '/' + 'Expand_FastDFS.json')
    else:
        config_list = yaml.get_config(basedir + '/' + 'FastDFS.json')
    
    if isinstance(config_list, int):
        print("Error!The configuration file that users fill is not the standard JSON format.")
        return 1 

    group_num = config_list[0]
    storage_num = config_list[2]
    tracker_num = str(config_list[3])

    group_storage_num = str(storage_num * group_num)

    cmd_check_nginx_num = "sh " + basedir + "/shell/check_status_num.sh" + ' ' + tracker_num + ' ' + group_storage_num
    code_active_pod = os.system(cmd_check_nginx_num)
    if code_active_pod != 0:
        return code_active_pod
    return code_active_pod


def check_expand():
    code_active_pod=check_expand_fastdfs()

    if code_active_pod != 0:
        return code_active_pod
    return code_active_pod

def check_status():
    code_active_pod=check_fastdfs()

    if code_active_pod!=0:
        print("Error! Pod number error of the cluster started by FastDFS+Nginx！")
        return code_active_pod
    else:
        print("Success! The number of Pod started by the cluster of FastDFS+Nginx is correct! Begin to detect whether the FastDFS+Nginx internal service is normal")

    cmd_dos2unix_check_shell = "/root/local/bin/kubectl exec -ti fastdfs-group0-storage0-0 dos2unix /etc/fdfs/check_fastdfs.sh >/dev/null 2>&1"
    os.system(cmd_dos2unix_check_shell)

    cmd_check_fastdfs_status="/root/local/bin/kubectl exec -ti fastdfs-group0-storage0-0 sh /etc/fdfs/check_fastdfs.sh"
    cmd_check_nginx0_status="/root/local/bin/kubectl exec -ti fastdfs-nginx-0 sh /nginx/fdfs_config/check_nginx.sh"
    cmd_check_nginx1_status="/root/local/bin/kubectl exec -ti fastdfs-nginx-1 sh /nginx/fdfs_config/check_nginx.sh"

    code_fastdfs_status=os.system(cmd_check_fastdfs_status)
    code_nginx0_status=os.system(cmd_check_nginx0_status)
    code_nginx1_status=os.system(cmd_check_nginx1_status)
    
    code_nginx_status=code_nginx0_status+code_nginx1_status
    if code_fastdfs_status!=0:
        print("Error! Internal service errors in FastDFS cluster" )
        return code_fastdfs_status
    if code_nginx_status!=0:
        print("Error! Internal service errors in Nginx cluster！")
        return code_nginx_status
    print("Success! All FastDFS&&Nginx clusters have been successfully launched!")
    return 0


if __name__=="__main__":
    code=check_status()
    print(code)
