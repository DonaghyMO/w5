#!/usr/bin/env python
# encoding:utf-8
# cython: language_level=3
from loguru import logger
import json
from elasticsearch import RequestsHttpConnection


async def scan(host, port, index, body, account, password):
    try:
        from elasticsearch import Elasticsearch
    except:
        logger.info("[ES] 导入 Elasticsearch 模块失败, 请输入命令 pip install elasticsearch")
        return {"status": 2, "result": "缺少 Elasticsearch 模块，请 pip install elasticsearch 安装"}

    logger.info("[ES] APP执行参数为：{host} {port} {index} {body}", host=host, port=port, index=index, body=body)

    try:
        if account != None and str(account) != "" and password != None and str(password) != "":

            es = Elasticsearch(hosts=["http://{}:{}@{}:{}/".format(account,password,host,port)])
        else:
            es = Elasticsearch(hosts=host)

        result = es.search(index=index, body=body)
    except Exception as e:
        return {"status": 2, "result": "ES连接失败:" + str(e)}
    return {"status": 0, "result": result}


async def insert(host, port, index, body, account, password):
    try:
        from elasticsearch import Elasticsearch
    except:
        logger.info("[ES] 导入 Elasticsearch 模块失败, 请输入命令 pip install elasticsearch")
        return {"status": 2, "result": "缺少 Elasticsearch 模块，请 pip install elasticsearch 安装"}

    logger.info("[ES] APP执行参数为：{host} {port} {index} {body}", host=host, port=port, index=index, body=body)

    try:
        if account != None and str(account) != "" and password != None and str(password) != "":

            es = Elasticsearch(hosts=["http://{}:{}@{}:{}/".format(account,password,host,port)])
        else:
            es = Elasticsearch(hosts=host)
        body = json.loads(body)
        if type(body) == dict:
            result = es.index(index=index, body=body)
        elif type(body) == list:
            for data in body:
                result = es.index(index=index, body=data)
        result = ""
    except Exception as e:
        return {"status": 2, "result": "ES连接失败:" + str(e)}
    return {"status": 0, "result": result}


if __name__ == "__main__":
    import asyncio

    # 插入
    # loop = asyncio.get_event_loop()
    # data = {'title': '美国留给伊拉克的是个烂摊子吗', 'url': 'http://view.news.qq.com/zt2011/usa_iraq/index.htm'}
    # result = loop.run_until_complete(insert("localhost",index="mo",body=data,account="elastic",password="*=Mot_0rR54aJnz3L+3X"))
    # print(result)

    # 查询

    dsl = {
        'query': {
            'match': {
                'title': '中国 领事馆'
            }
        }
    }

    # 实验室es
    # result = loop.run_until_complete(
    #     scan("http://192.168.114.1:9200", index="mo", body=dsl, account="wangxinyu", password="76VypLzXiHwJ23"))
    # print(result)

    # 本地es
    # loop = asyncio.get_event_loop()
    # result = loop.run_until_complete(
    #     scan("localhost","9200", index="mo", body=dsl, account="elastic", password="*=Mot_0rR54aJnz3L+3X"))
    # print(result)

    # 测试批量导入数据
    datas =[
    {
        "title": "美国留给伊拉克的是个烂摊子吗",
        "url": "http://view.news.qq.com/zt2011/usa_iraq/index.htm",
        "date": "2011-12-16"
    },
    {
        "title": "公安部：各地校车将享最高路权",
        "url": "http://www.chinanews.com/gn/2011/12-16/3536077.shtml",
        "date": "2011-12-16"
    },
    {
        "title": "中韩渔警冲突调查：韩警平均每天扣1艘中国渔船",
        "url": "https://news.qq.com/a/20111216/001044.htm",
        "date": "2011-12-17"
    },
    {
        "title": "中国驻洛杉矶领事馆遭亚裔男子枪击 嫌犯已自首",
        "url": "http://news.ifeng.com/world/detail_2011_12/16/11372558_0.shtml",
        "date": "2011-12-18"
    }
]
    from elasticsearch import Elasticsearch
    account = "wangxinyu"
    password = "76VypLzXiHwJ23"
    host = "192.168.114.1"
    port = "9200"
    es = Elasticsearch(hosts=["http://{}:{}@{}:{}/".format(account,password,host,port)])

    # 设置mapping
    mapping = {
        'properties': {
            'title': {
                'type': 'text',
                'analyzer': 'ik_max_word',
                'search_analyzer': 'ik_max_word'
            }
        }
    }
    dsl = {
        'query': {
            'match': {
                'title': '中国 领事馆'
            }
        }
    }
    # es.indices.delete(index='news', ignore=[400, 404])
    # for data in datas:
    #     res = es.index(index='new', body=data)
    #     print(res)
    res = es.search(index='new', body=dsl,ignore=400)
    print(res)
    # result = es.indices.put_mapping(index='news', doc_type='politics', body=mapping)


    # 插入
    # es.index(index="mo", doc_type="politics",body=data)

    # https的es服务的导入方式
    # es = Elasticsearch(
    #     [host],
    #     http_auth=(account, password),
    #     scheme="https",
    #     port=int(port),
    #     # ssl_context=context,
    #     use_ssl=True,
    #     verify_certs=False,
    #     connection_class=RequestsHttpConnection,
    # )
