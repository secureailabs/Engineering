'''
Secure AI Labs
Jingwei Zhang
jingwei@secureailabs.com

A simple script to deploy log and system metrics monitoring services.
'''

import paramiko
import yaml
import json
import argparse
import time
import http.client


def CreateSSHChannel(username, password, server):
    '''
    open a ssh channel for newly spawned vm
    username(str): ssh login username
    password(str): ssh login password
    server(str): vm ip 
    '''
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(server, username=username, password=password)
    return ssh


def EnvironmentInit():
    '''
    install prerequisite packages
    '''
    command = "sudo apt install unzip;"
    return command


def GetNodeExporter(command):
    '''
    install exporter
    '''
    command += "wget https://github.com/prometheus/node_exporter/releases/download/v1.3.1/node_exporter-1.3.1.linux-amd64.tar.gz;"
    command += "tar -zxvf node_exporter-1.3.1.linux-amd64.tar.gz;"
    return command


def GetPromtail(command):
    '''
    install promtail
    '''
    command += "wget https://github.com/grafana/loki/releases/download/v2.4.1/promtail-linux-amd64.zip;"
    command += "unzip promtail-linux-amd64.zip;"
    return command


def RunPromtail(ch):
    '''
    initiate promtail service
    '''
    command = "sudo ./promtail-linux-amd64 -config.file=promtail-local-config.yaml &> promlog.log & "
    ch.exec_command(command)


def RunNodeExporter(ch):
    '''
    initiate exporter service
    '''
    command = "sudo ./node_exporter-1.3.1.linux-amd64/node_exporter &> node_exporter.log &"
    ch.exec_command(command)


def ConfigPromtail(command, config):
    '''
    generate promtail config file
    '''
    command += "printf \"" + config + "\" > promtail-local-config.yaml;"
    return command


def GenerateConfigJson(filename, prometheusIP):
    '''
    create promtail config file
    '''
    f = open(filename, 'r')
    config = f.read()
    config = yaml.load(config)
    config['clients'][0]['url'] = "http://" + prometheusIP + ":3100/loki/api/v1/push"
    stdoutlog = {'job_name': 'vmlog',
                 'static_configs': [{'targets': ['localhost'],
                                     'labels': {'job': 'joblogs',
                                                '__path__': '/root/VmImageInit.log'
                                                }
                                     }
                                    ]
                 }
    config['scrape_configs'].append(stdoutlog)
    config = yaml.dump(config)
    f.close()
    return config


def SubmitNewConfigToServer(url, ip):
    '''
    add new vm ip to prometheus server
    '''
    connection = http.client.HTTPConnection(url, 9999)
    payload = json.dumps({'ip': ip, 'port': '9100'})
    headers = {
        'Content-Length': str(len(payload))
    }
    connection.request('POST', '', payload, headers)
    response = connection.getresponse()
    print(response.read().decode())


def DeployAll(ips, username, password, serverIP, configFile):
    '''
    deploy services
    '''
    channel = []
    for ip in ips:
        channel.append(CreateSSHChannel(username, password, ip))
        SubmitNewConfigToServer(serverIP, ip)
    config = GenerateConfigJson(configFile, serverIP)
    for ch in channel:
        command = EnvironmentInit()
        command = GetNodeExporter(command)
        command = GetPromtail(command)
        command = ConfigPromtail(command, config)
        ch.exec_command(command)
        time.sleep(3)
        RunPromtail(ch)
        RunNodeExporter(ch)
        time.sleep(2)
        ch.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', nargs='*')
    parser.add_argument('-u', type=str)
    parser.add_argument('-p', type=str)
    parser.add_argument('-s', type=str)
    parser.add_argument('-c', type=str)

    args = parser.parse_args()

    clientIPs = args.i
    username = args.u
    password = args.p
    serverIP = args.s
    configFile = args.c

    DeployAll(clientIPs, username, password, serverIP, configFile)
