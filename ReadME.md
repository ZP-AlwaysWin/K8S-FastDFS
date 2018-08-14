## Docker化FastDFS组件使用说明：

### 一.配置文件详解：

一期中配置文件json的标准格式如下：
```
{
    "node_hosts": ["172.20.0.95","172.20.0.96","172.20.0.97"],
    "TRACKER_SERVER_NUM": 2,
    "GROUP_NUM": 1,
    "STORAGE_NUM": 3,
    "FASTDFS_DATA": 5
}
```

对其中参数填写说明如下：

1. node_hosts：
	要求必须填写合法Kubernetes node节点IP,且去掉重复的之后的IP个数不能少于两个
	
2. TRACKER_SERVER_NUM：
	其中TRACKER_SERVER_NUM目前不使用，为二期预留的配置选项，不可以修改

3. GROUP_NUM：
	FastDFS组的个数，目前一期中，只允许填写1、2、3组，且其填写类型必须是大于0的int类型。
4. STORAGE_NUM：
	每个FastDFS组下的Storage的个数，其填写类型必须是大于0的int类型，且不能大于node_hosts的去重个数。
5. FASTDFS_DATA:
	每个FastDFS组下的Srorage的挂载磁盘的大小，目前其填写类型必须是大于0小于等于5的int类型
	
### 二.使用说明：

1.安装FastDFS集群，按照要求修改FastDFS文件夹下的FastDFS.json配置文件，然后运行FastDFS文件夹下的ChangeYaml.py脚本；
	`python ChangeYaml.py`

2.安装FastDFS集群之后，检测集群是否运行正常，运行FastDFS文件夹下的check_fastdfs.py脚本；
	`python check_fastdfs.py`

3.扩充FastDFS节点，修改FastDFS/json下的Expand_FastDFS.json扩充节点的配置文件。

```
{
    "node_hosts": ["172.20.0.95","172.20.0.96","172.20.0.97"],
    "TRACKER_SERVER_NUM": 2,
    "GROUP_NUM": 1,
    "STORAGE_NUM": 3,
    "FASTDFS_DATA": 5
}
```
**注意:**
扩充FastDFS节点只允许修改GROUP_NUM和FASTDFS_DATA的value值

(1). FASTDFS_DATA:
	每个FastDFS组下的Srorage的挂载磁盘的大小，目前其填写类型必须是大于0小于等于5的int类型

(2). GROUP_NUM：
	FastDFS组的个数，目前一期中，只允许填写1、2、3组，且其填写类型必须是大于目前现有组数的int类型。	
	
按要求修改配置文件结束后，运行FastDFS文件夹下的Expand_Node.py脚本
		python Expand_Node.py

4.扩充FastDFS集群之后，检测集群是否运行正常，运行FastDFS文件夹下的check_fastdfs.py脚本；
	`python check_fastdfs.py`
	
5. 删除FastDFS集群，运行FastDFS文件夹下的DelClu.py脚本
	`python DelClu.py`
	
