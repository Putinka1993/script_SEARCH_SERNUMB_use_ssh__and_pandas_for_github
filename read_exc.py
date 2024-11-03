

import paramiko
import re
import pandas as pd

print('start')

df = pd.read_excel('/home/astra/Документы/SN_SEARCH/S-NSSD.xlsx', sheet_name='Лист4')

# hostname = '10.108.61.86'#'zhukov-iv'
# hostname = '10.108.61.107'#'lipkin-va'
# hostname = '10.108.61.83'#sukhov
# hostname = '10.108.61.80'#sidoricheva
# hostname = '10.108.61.90'#gaidukova
# hostname = '10.108.61.10' #golubev-vl-l
hostname = '10.108.61.111' #usova


username = input()
password = input()

command_4 = "lsblk -o SERIAL,SIZE,ROTA,VENDOR,MODEL | tail -n +2 | awk '{printf \"%s | %s | %s | %s %s\\n\", $1, $2, ($3==0 ? \"SSD\" : \"HDD\"), $4, $5}'"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

result = ''

try:
    
    ssh.connect(hostname=hostname, username=username, password=password)
    print('CONNECT')
    channel = ssh.get_transport().open_session()
    channel.get_pty()

    channel.exec_command(command_4)
    print('USE COMMAND')
    channel.send(f"{password}\n")
    print('USE PASSW')

    while True:
        if channel.recv_ready():
            result += str(channel.recv(1024).decode('utf-8'))

        if channel.exit_status_ready():
            break
    
finally:
    ssh.close()
    channel.close()
    print('CLOSE SSH')
    print('----FINISH get_SN----')
print(result)

lines = result.splitlines()
del lines[0]

print('PRINT LINES')
print(lines)

SN = ''
SIZE = ''
TYPE_HD = ''
MODEL = ''
for row in lines:
    if '|' in row:
        if int( re.sub(r'\D', '', row.split(' | ')[1]) ) > 0:
            print('PRINT LINES')
            print(row)