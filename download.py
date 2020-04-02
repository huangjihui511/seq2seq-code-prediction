import pymysql
from sshtunnel import SSHTunnelForwarder

mypkey = paramiko.RSAKey.from_private_key_file("/Users/***/.ssh/id_rsa")
with SSHTunnelForwarder(
     ('web.ghtorrent.org', 3306), 
        ssh_username="ghtorrent",  
        ssh_pkey=mypkey, 
        ssh_private_key_password="*****",#my password for my pc
        remote_bind_address=('web.ghtorrent.org', 3306)) as server:  
    conn = pymysql.connect(host='127.0.0.1', 
                       port=server.local_bind_port,
                       user='ght', 
                       passwd='', 
                       db='ghtorrent')