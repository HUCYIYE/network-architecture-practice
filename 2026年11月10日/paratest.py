
import paramiko
import time
from getpass import getpass

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(
    hostname="10.1.1.1",
    port=22,
    username="python",
    password=getpass("Password: "),
    look_for_keys=False,
    allow_agent=False
)

shell = ssh.invoke_shell()
time.sleep(1)

if shell.recv_ready():
    shell.recv(65535)

shell.send("screen-length 0 temporary\n")
time.sleep(1)

if shell.recv_ready():
    shell.recv(65535)

shell.send("display device\n")
time.sleep(2)

output = b""
while shell.recv_ready():
    output += shell.recv(65535)

print(output.decode(errors="ignore"))

ssh.close()
