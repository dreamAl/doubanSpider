import pymysql
import random

from Util.Ping import check_proxy


class Mysql(object):

    def __init__(self):
        self.connect = pymysql.Connect(user='root', passwd="aywan0327", host='127.0.0.1', port=3306,
                                       database='education')
        self.cursor = self.connect.cursor()
        self.connect.autocommit(True)

    def data_counts(self):
        self.cursor.execute("select count(id) from proxy")
        counts = self.cursor.fetchone()[0]
        return counts

    def get_proxy(self):
        counts = self.data_counts()
        id = random.randint(1, counts)
        query_proxy = "select proxy_ip, proxy_port, proxy_type from proxy where id = %s and is_delete = 1" % id
        self.cursor.execute(query_proxy)
        print("exexute sql: %s" % query_proxy)
        proxy = self.cursor.fetchone()
        if not proxy:
            self.get_proxy()
        # print("proxy info is %s,%s,%s" % proxy)
        proxy_info = "%s://%s:%s" % (proxy[2].lower(),proxy[0],proxy[1])
        if check_proxy(proxy[2], proxy_info) != 'OK':
            self.delete_data(proxy[0])
            self.get_proxy()
        print("using %s" % proxy_info)
        return proxy_info

    def delete_data(self, ip):
        if ip:
            delete_sql = 'delete from proxy where proxy_ip ="%s"' % ip
            # delete_sql = 'update proxy set is_delete = 0 where proxy_ip = "%s"' % ip
            self.cursor.execute(delete_sql)
            print("execute sql: %s" % delete_sql)

    def close(self):
        self.cursor.close()
        self.connect.close()


if __name__ == '__main__':
    client = Mysql()
    client.data_counts()
    ip = client.get_proxy()
    print(ip)
