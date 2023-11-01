import paramiko
import configparser


def get_login_info(config_name):
    """
    通过config_name作为section去./config.ini中招参数
    :param config_name:
    :return:
    """
    cf = configparser.RawConfigParser()
    cf.read("./config.ini")
    username = cf.get(config_name, "username")
    key_file = cf.get(config_name, "key_file")
    password = cf.get(config_name, "password")
    host = cf.get(config_name, "host")
    port = cf.get(config_name, "port")

    return username, password, key_file, host, port


def execute_remote_command(command):
    # 获取配置
    username, password, key_filename, server, port = get_login_info("119.91.228.150")
    port = int(port) if port else 22

    # 创建 SSH 客户端
    ssh_client = paramiko.SSHClient()

    # 允许连接到未知主机时自动添加条目到 known_hosts 文件
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if not password and not key_filename:
            raise Exception("你没有输入密码或者密钥文件")
        # 连接到远程服务器
        if password:
            ssh_client.connect(server, username=username, password=password)
        elif key_filename:
            ssh_client.connect(server, port=port, username=username, key_filename=key_filename)

        # 执行命令
        stdin, stdout, stderr = ssh_client.exec_command(command)

        # 获取命令执行的输出
        output = stdout.read().decode()
        error = stderr.read().decode()

        if output:
            return f"Command output: {output}"
        if error:
            return f"Command error: {error}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

    finally:
        # 关闭 SSH 连接
        ssh_client.close()


if __name__ == '__main__':
    # 用法示例
    execute_remote_command("whoami")
