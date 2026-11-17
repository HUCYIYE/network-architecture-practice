import telnetlib
import paramiko
import time
import os

ips = ["10.10.1.1", "10.10.1.2", "10.10.1.3",
       "10.10.1.4", "10.10.1.5"]

user = "python"
password = "Huawei@123"

folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(folder, exist_ok=True)


def save(ip, mode, text):
    print(text)
    name = os.path.join(folder, mode + "_" + ip + ".txt")
    with open(name, "w", encoding="utf-8") as f:
        f.write(text)


def read_ssh(channel):
    data = b""
    start = time.time()

    while time.time() - start < 30:
        if channel.recv_ready():
            part = channel.recv(65535)
            if not part:
                raise ConnectionError("SSH closed")
            data += part
            if data.rstrip().endswith(b">"):
                return data.decode("utf-8", errors="replace")
        elif channel.closed:
            raise ConnectionError("SSH closed")

        time.sleep(0.1)

    raise TimeoutError("SSH timeout")


def AutoTelnet():
    commands = [
        "undo ter mon",
        "screen-l 0 t",
        "dis ip int br",
        "dis cpu-usage",
        "dis logb slot 0"
    ]

    for ip in ips:
        tn = None
        text = "\nTelnet " + ip + "\n"

        try:
            tn = telnetlib.Telnet(ip, 23, timeout=10)

            if b"Username:" not in tn.read_until(b"Username:", 10):
                raise TimeoutError("No user prompt")
            tn.write((user + "\n").encode())

            if b"Password:" not in tn.read_until(b"Password:", 10):
                raise TimeoutError("No pwd prompt")
            tn.write((password + "\n").encode())

            data = tn.read_until(b">", 20)
            text += data.decode("utf-8", errors="replace")

            if not data.rstrip().endswith(b">"):
                raise ConnectionError("Login failed")

            for cmd in commands:
                tn.write((cmd + "\n").encode())
                data = tn.read_until(b">", 30)
                result = data.decode("utf-8", errors="replace")
                text += "\n" + result

                if not data.rstrip().endswith(b">"):
                    raise TimeoutError("Cmd timeout")
                if "Error:" in result:
                    text += "\nCmd error\n"

        except Exception as e:
            text += "\nFailed: " + str(e)

        finally:
            if tn is not None:
                tn.close()

        save(ip, "telnet", text)


def AutoPara():
    commands = [
        "undo ter mon",
        "screen-l 0 t",
        "dis dev",
        "dis ver",
        "dis clo"
    ]

    for ip in ips:
        ssh = None
        text = "\nSSH " + ip + "\n"

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            ssh.connect(
                ip,
                username=user,
                password=password,
                timeout=10,
                banner_timeout=20,
                auth_timeout=20,
                look_for_keys=False,
                allow_agent=False
            )

            channel = ssh.invoke_shell()
            text += read_ssh(channel)

            for cmd in commands:
                channel.sendall((cmd + "\n").encode())
                result = read_ssh(channel)
                text += "\n" + result

                if "Error:" in result:
                    text += "\nCmd error\n"

        except Exception as e:
            text += "\nFailed: " + str(e)

        finally:
            if ssh is not None:
                ssh.close()

        save(ip, "ssh", text)


def AutoManageDevice(LibName):
    LibName = LibName.strip().lower()

    if LibName == "telnetlib":
        AutoTelnet()
    elif LibName == "paramiko":
        AutoPara()
    else:
        print("Invalid lib")


if __name__ == "__main__":
    name = input("Lib (telnetlib/paramiko): ")
    AutoManageDevice(name)