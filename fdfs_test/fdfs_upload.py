# -*- coding:utf-8 -*-
from fdfs_client.client import *
import time
 
client_file='client.conf'
test_file='client.conf'
download_file='client.conf'
 
try:
    client = Fdfs_client(client_file)
    #upload
    ret_upload = client.upload_by_filename(test_file)
    print ret_upload
    time.sleep(5)   #等待5s，否则下载时会报错文件不存在
    file_id=ret_upload['Remote file_id'].replace('\\','/')  #新版本文件存放Remote file_id格式变化
     
    #download
    ret_download=client.download_to_file(download_file,file_id)
    print ret_download
     
    #delete
    ret_delete=client.delete_file(file_id)
    print ret_delete
     
except Exception,ex:
    print ex 
