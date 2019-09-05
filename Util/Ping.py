import os
import requests


def pingIp(ip):
    ret = os.popen("ping %s" % ip).read()
    print("ping %s..." % ip)
    if "TTL" in ret and "ms" in ret:
        print("%s is good" % ip)
        return True
    else:
        return False


def check_proxy(proxy_type, proxy):
    proxy_handle = {proxy_type: proxy}
    response = requests.get("https://xa.zu.anjuke.com/fangyuan/p1/", proxies=proxy_handle)
    # print(response.raw)
    return response.reason


if __name__ == '__main__':
    import base64
    proxy = "http://116.255.161.203:16816"
    user_passwd = "1093993119:8604ioz2".encode('utf-8')
    # 对账户密码进行base64编码转换
    base64_userpasswd = base64.b64encode(user_passwd)
    # 对应到代理服务器的信令格式里
    print('Basic ' + base64_userpasswd.decode())
