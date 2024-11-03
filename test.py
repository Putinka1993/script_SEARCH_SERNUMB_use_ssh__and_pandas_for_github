import paramiko
import re
import pandas as pd


df = pd.read_excel('/home/astra/Документы/SN_SEARCH/S-NSSD.xlsx', sheet_name='Лист3')


print('start')
# hostname = '10.108.61.86'#'zhukov-iv'
# hostname = '10.108.61.107'#'lipkin-va'
# hostname = '10.108.61.83'#sukhov
# hostname = '10.108.61.80'#sidoricheva
hostname = '10.108.61.90'#gaidukova
# hostname = '10.108.61.10' #golubev-vl-l

username = 'astra'
password = 'RE@kos2022'

command_1 = 'lsblk -o NAME,SERIAL'
command_2 = 'sudo dmidecode -t system | grep Serial'
command_3 = 'lsblk -o NAME,SERIAL,SIZE,ROTA,TYPE,MODEL'
command_4 = "lsblk -o SERIAL,SIZE,ROTA,VENDOR,MODEL | tail -n +2 | awk '{printf \"%s | %s | %s | %s %s\\n\", $1, $2, ($3==0 ? \"SSD\" : \"HDD\"), $4, $5}'"


class get_SN_PC:

    def __init__(self, hostname, username, password, command) -> None:
        self.hstn = hostname
        self.usrn = username
        self.pssw = password
        self.cmd = command

    def get_SN(self):

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        result = ''

        channel = None

        try:
            ssh.connect(self.hstn, username=self.usrn, password=self.pssw)

            print(f'1 CONNECT - |{self.hstn}|')
            channel = ssh.get_transport().open_session()
            print('2 GET TRANSPORT')
            channel.get_pty()
            print('3 GET PTY')

            channel.exec_command(self.cmd)
            print('4 USE COMMAND')
            channel.send(f"{self.pssw}\n")
            print('5 USE PSW')
            while True:
                if channel.recv_ready():
                    result += str(channel.recv(1024).decode('utf-8'))

                if channel.exit_status_ready():
                    break
        except paramiko.ssh_exception.NoValidConnectionsError:
            print(f'ERROR CONNECT {self.hstn}')
        # except paramiko.SSHException as e:
        #     print(f'ERRRRORRRRR {e}')
        # except Exception as e:
        #     print(f'OOOPSSS ERRROR {e}')

        finally:
            if channel:
                channel.close()
            # ssh.close()
        # print(result)
        return result

# SN_pc = get_SN_PC(hostname, username, password, command_4)
# result = SN_pc.get_SN()

# lines = result.splitlines()

# del lines[0]

# SN = ''
# SIZE = ''
# TYPE_HD = ''
# MODEL = ''
# for row in lines:
#     if int( re.sub(r'\D', '', row.split(' | ')[1]) ) > 0:
#         info_hd = row.split('|')
#         SN_pc += ' ' + info_hd[0]
#         SIZE += ' ' + info_hd[1]
#         TYPE_HD += ' ' + info_hd[2]
#         MODEL += ' ' + info_hd[3]




def _apply(row):
    list_data = []
    list_data.append(row['room'])
    list_data.append(row['ip'])
    list_data.append(row['account_name'])
    list_data.append(row['name'])

    SN_pc = get_SN_PC(row['ip'], username, password, command_4)
    result = SN_pc.get_SN()

    lines = result.splitlines()
    
    if lines:
        del lines[0]

    SN = ''
    SIZE = ''
    TYPE_HD = ''
    MODEL = ''
    print(lines)
    for row in lines:
        if '|' in row:
            if int( re.sub(r'\D', '', row.split(' | ')[1]) ) > 1:
                print(f'right {row}')
                info_hd = row.split('|')
                SN += info_hd[0] + ', '
                SIZE += info_hd[1] + ', '
                TYPE_HD += info_hd[2] + ', '
                MODEL += info_hd[3] + ', '
    
    list_data.append(SN)
    list_data.append(SIZE)
    list_data.append(TYPE_HD)
    list_data.append(MODEL)
    return list_data

result = df.apply(_apply, axis=1)

columns = ['place', 'ip', 'account_name', 'name', 'SN_HD', 'SIZE', 'TYPE_HD', 'MODEL']
data = []
for el in result:
    data.append(el)



df_result = pd.DataFrame(data=data, columns=columns)
print(df_result)

df_result.to_excel('temp.xlsx', index=False)








# print(test_dict)

# print(f'name - {result[34], result[35]}, serial - {result[25]}, ssd/hdd - {result[55]}, SIZE - {result[28]}')

# print(f'{result[]}')

# -------------------------
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

# try:
#     ssh.connect(hostname, username=username, password=password)

#     stdin, stdout, stderr = ssh.exec_command(command_2)

#     result = stdout.read()#.decode()

# finally:
#     ssh.close()

# print('finish')

# # print(str(result).split('\\'))
# print(result.decode())

# # print(result.split('    ')[3])
# # for el in result:
#     # print(el)