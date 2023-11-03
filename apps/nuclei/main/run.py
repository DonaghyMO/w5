#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger


async def execute(host, command):
    try:
        from my_tools.ssh_clients.ssh_client import execute_remote_command
    except:

        return {"status": 2, "result": "导入ssh_client模块失败"}

    logger.info("[Linux远程命令【nuclei】] APP执行参数为：{host} {command}", host=host, command=command)

    result = execute_remote_command(command, host)

    return {"status":0,"result":result}


