#!/usr/bin/env python

import paramiko
import os
import getpass
from datetime import datetime
import logging

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

hosts = open(r'IPAddressList.txt', 'r')
commands = open(r'commands.txt','r')
day = datetime.today()

time = day.strftime('%H%M')
dirname = day.strftime('%Y%m%d')

if not os.path.exists(dirname):
    os.makedirs(dirname)

username = raw_input("Username: ")
password = getpass.getpass()
multiple_files = raw_input("Do you need output in multiple files: ")

if multiple_files is ("Y","y"):
    for host in hosts:
        host = host.replace("\n","")
        try:
            ssh.connect(host, username=username, password=password)
        except Exception as e:
            logging.error(host+":   "+str(e))
            continue
        output = open(dirname + '/' + host + '-' + time + '.txt', 'w')
        output.write("\n###################################### >> " + host + " << ######################################\n\n")
        commands.seek(0,0)
        for command in commands:
            stdin, stdout, stderr = ssh.exec_command(command)
            output.write(stdout.read())
            output.close()
else:
    output = open(dirname + '/output-' + time + '.txt', 'w')
    for host in hosts:
        host = host.replace("\n","")
        try:
            ssh.connect(host, username=username, password=password)
            print host+"    OK"
            output.write("\n###################################### >> " + host + " << ######################################\n\n")
            commands.seek(0,0)
            for command in commands:
                stdin, stdout, stderr = ssh.exec_command(command)
                output.write(stdout.read())

        except Exception as e:
            logging.error(host+":   "+str(e))
            continue
    output.close()
hosts.close()
commands.close()
ssh.close()
