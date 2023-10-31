# from loguru import logger
import json
import re
import nmap
import subprocess
import socket
import subprocess
from scan_and_attack.ssh_clients import *

async def ip_detect(ips, ports):
    # logger.info("[批量ip探测] APP 执行参数为: ip地址:{ips} 探测端口:{ports}", ips=ips,ports=ports)
    # ip处理
    ips = ips.strip()
    ips = [ip for ip in ips.split(',')]
    # 由于有一些ip禁ping，尝试连接用户指定端口（未填时是用默认端口80,22,8080,3060,3306）
    # 端口处理
    ports = ports.strip()
    # ports为空时默认扫描22,80,8080,3306,8888,8090
    if not ports:
        ports = "22,80,8080,3306,8888,8090"

    result = run_from_cmd(ips,ports)
    # 进行es存储

    return {"status":0,"result":json.dumps(result)}

def run_from_cmd(ips,ports):
    """
    用命令行运行
    :param ips:
    :param ports:
    :return:
    """
    results = {}
    for ip in ips:


        # 要执行的系统命令
        command = """sudo -u mo nmap -v {ip} -p {ports}|grep -E \"^PORT|^[0-9]+/tcp|^[0-9]+/udp\"""".format(ip=ip,ports=ports)  # 这里以在 Unix/Linux 系统中列出当前目录的文件为例

        # 使用subprocess.run()执行命令
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # 打印命令的标准输出和标准错误输出
        print("标准输出：")
        print(result.stdout)

        print("标准错误输出：")
        print(result.stderr)

        # 打印命令的返回码
        print("返回码:", result.returncode)
        results.update({ip:result.stdout})
    return(results)


def run_from_python(ips,ports):
    """
    用python运行
    :param ips:
    :param ports:
    :return:
    """
    results = ""
    for ip in ips:
        nm = nmap.PortScanner()
        nm.scan(ip, ports)
        results += """
        执行命令：{command}
        扫描相关信息：{scan_info}
        所有host：{all_hosts}

        """.format(command=nm.command_line(), scan_info=nm.scaninfo(), all_hosts=nm.all_hosts())
        for i in nm.all_hosts():
            results += "{ip}：{info}".format(ip=i, info=nm[i])
    return {"status": 0, "result": results}


if __name__ == "__main__":
    print(execute_remote_command("whoami"))

