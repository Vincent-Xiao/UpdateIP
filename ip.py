'''
****************************************Copyright (c)**************************************************
**                                        ICT
**                                     
**---------------------------------------File Info-----------------------------------------------------
** File name:           ip.py
** Last modified Date:  xx-xx-xx
** Last Version:        1.0
** Descriptions:        xxxxxxxxxxxxxxxxxx
**------------------------------------------------------------------------------------------------------
** Created by:          vincent
** Created date:        2018-02-05 
** Version:             1.0
** Descriptions:        auto get and update ip address of localhost to servers
**------------------------------------------------------------------------------------------------------
** Modified by:         user-name
** Modified date:        x-x-x    
** Version:             1.0
** Descriptions:        xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
**
**------------------------------------------------------------------------------------------------------
********************************************************************************************************
'''
# -*- coding: utf-8 -*-
import os
import time
import socket
import base64
import paramiko

IP='IP'
User='User'
Passwd='passwd'
Dir='~/ip_server/mac'
File=Dir+'/'+'ip.txt'

def main():
    client = paramiko.SSHClient()
    ip=get_host_ip()
    updteIP(client,ip)
    while 1:
        new_ip=get_host_ip()
        print new_ip
        if new_ip !=ip:
            updteIP(client,new_ip)
        time.sleep(600)

def updteIP(client,ip):
    try:
        ssh_connect(client)
        ssh_createFile(client)
        ssh_writeIP(client,ip)
    finally:
        ssh_close(client)

def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #ipv4
        #s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) #ipv6
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip

def ssh_connect(client):
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(IP, username=User, password=Passwd)
    print 'ssh connected'

def ssh_createFile(client):
    stdin, stdout, stderr = client.exec_command('mkdir -p '+Dir)
    stdin, stdout, stderr = client.exec_command('rm -f '+File)
    stdin, stdout, stderr = client.exec_command('touch '+File)

def ssh_writeIP(client,ip):
    stdin, stdout, stderr = client.exec_command('echo '+ip+' > ' + File)
    stdin, stdout, stderr = client.exec_command('cat '+ File)
    print stdout.readlines()

def ssh_close(client):
    client.close()
    print 'ssh closed'


if __name__ == "__main__" :
    main()
