import paramiko
import time
from datetime import datetime

switches = [
    {"name": "TJ-CS01-yulongwu", "ip": "10.1.1.1", "username": "yulongwu", "password": "Datacom@168"},
    {"name": "TJ-AS01-yulongwu", "ip": "10.1.1.2", "username": "yulongwu", "password": "Datacom@168"},
    {"name": "TJ-AS02-yulongwu", "ip": "10.1.1.3", "username": "yulongwu", "password": "Datacom@168"}
]

commands = ["dis version", "dis cpu", "dis memory", "dis int br"]

date = datetime.now().strftime("%Y-%m-%d")

for switch in switches:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(switch["ip"], username=switch["username"], password=switch["password"], look_for_keys=False, allow_agent=False, timeout=10)

    shell = ssh.invoke_shell()
    time.sleep(2)
    shell.recv(65535)

    shell.send("screen-length 0 temporary\n")
    time.sleep(2)
    shell.recv(65535)

    filename = switch["name"] + "_" + date + "_巡检.txt"
    file = open(filename, "w", encoding="utf-8")

    print("Name:", switch["name"], file=file)
    print("IP:", switch["ip"], file=file)
    print("Date:", date, file=file)

    for command in commands:
        shell.send(command + "\n")
        time.sleep(3)

        print("=" * 60, file=file)
        print(command, file=file)

        while shell.recv_ready():
            output = shell.recv(65535).decode(errors="ignore")
            print(output, file=file)
            time.sleep(0.2)

    file.close()
    ssh.close()
    print(switch["name"], "OK")