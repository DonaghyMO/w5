#!/usr/bin/env python
# encoding:utf-8
from loguru import loggerfrom


async def hello_world(name):
    logger.info("[Hello World] APP 执行参数为: {name}", name=name)
    return {"status": 0, "result": "Hello," + str(name)}

if __name__ == '__main__':
    import sys
    sys.path.append("/w5/my_tool")
    print(ssh_client.ssh_clients.execute_remote_command("whoami"))