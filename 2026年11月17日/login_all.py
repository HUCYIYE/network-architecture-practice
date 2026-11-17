#powered by codex ↓↓↓
import sys
import re
import time
import subprocess

USERNAME = "python"
PASSWORD = "Huawei@123"

# 华为用户视图提示符，例如 <BJ-CE1-yulongwu>
PROMPT = re.compile(rb"<[^<>\r\n]+>\s*$")


def login_telnet(ip):
    import telnetlib

    tn = telnetlib.Telnet(ip, 23, timeout=15)
    try:
        index, _, _ = tn.expect(
            [rb"(?i)(?:username|login)\s*:"], timeout=15
        )
        if index < 0:
            raise RuntimeError("没有收到用户名提示")

        tn.write((USERNAME + "\n").encode())

        index, _, _ = tn.expect(
            [rb"(?i)password\s*:"], timeout=15
        )
        if index < 0:
            raise RuntimeError("没有收到密码提示")

        tn.write((PASSWORD + "\n").encode())

        index, _, output = tn.expect(
            [
                PROMPT,
                rb"(?i)(?:authentication fail|incorrect|login fail)"
            ],
            timeout=20
        )

        print(output.decode("utf-8", errors="replace"))
        if index != 0:
            raise RuntimeError("登录失败或等待提示符超时")

        input("\n登录成功，请截图。按回车断开连接并关闭窗口……")
    finally:
        tn.close()


def login_ssh(ip):
    import paramiko

    client = paramiko.SSHClient()

    # 仅用于本次课程实验，自动接受首次连接的设备密钥
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(
            hostname=ip,
            port=22,
            username=USERNAME,
            password=PASSWORD,
            timeout=15,
            banner_timeout=20,
            auth_timeout=20,
            look_for_keys=False,
            allow_agent=False
        )

        channel = client.invoke_shell()
        output = b""
        deadline = time.monotonic() + 20

        while time.monotonic() < deadline:
            if channel.recv_ready():
                data = channel.recv(65535)
                if not data:
                    raise RuntimeError("SSH连接已断开")

                output += data
                print(
                    data.decode("utf-8", errors="replace"),
                    end="",
                    flush=True
                )

                if PROMPT.search(output):
                    break
            elif channel.closed:
                raise RuntimeError("SSH通道已关闭")
            else:
                time.sleep(0.1)
        else:
            raise TimeoutError("等待设备提示符超时")

        input("\n\n登录成功，请截图。按回车断开连接并关闭窗口……")
    finally:
        client.close()


def main():
    # 子窗口：自动登录指定设备
    if len(sys.argv) == 4 and sys.argv[1] == "--worker":
        mode, ip = sys.argv[2], sys.argv[3]

        print("=" * 55)
        print("连接方式：", mode.upper())
        print("目标地址：", ip)
        print("登录用户：", USERNAME)
        print("=" * 55, flush=True)

        try:
            if mode == "telnet":
                login_telnet(ip)
            else:
                login_ssh(ip)
        except Exception as error:
            print("\n连接失败：", type(error).__name__, str(error))
            input("\n按回车关闭窗口……")
        return

    # 主窗口：一次打开五个自动登录窗口
    mode = input("输入 telnet 或 ssh：").strip().lower()

    if mode not in ("telnet", "ssh"):
        print("只能输入 telnet 或 ssh")
        return

    for number in range(1, 6):
        subprocess.Popen(
            [
                sys.executable,
                __file__,
                "--worker",
                mode,
                "10.10.1." + str(number)
            ],
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )


if __name__ == "__main__":
    main()