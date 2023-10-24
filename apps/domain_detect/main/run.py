from loguru import logger
import socket


async def query(domain):
    logger.info("[Domain Detect] APP执行参数为: {domain}",domain=domain)
    ips = socket.gethostbyname_ex(domain)[-1]
    ips = ",".join(ips)
    return {"status":0, "result":ips}
def get_host_from_file(domain):
    for url in domain:
        url = url.strip()
        result = []
        try:
            ips = socket.gethostbyname_ex(url)[-1]
            result.append(url + '\t' + ';'.join(ips) + '\t' + 'ping' + '\n')
        except Exception as e:
            print(url, e)
        print()