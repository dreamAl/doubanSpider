from pymongo import MongoClient
import pandas as pd


class MongoDb(object):

    def __init__(self, database, collection):
        self.mongo = MongoClient(host='127.0.0.1', port=27017)
        self.database = self.mongo[database]
        self.collection = self.database[collection]

    def insert(self, data):
        self.collection.insert(data)

    def close(self):
        self.mongo.close()

    def delete_data(self):
        self.collection.drop()

    def query(self):
        """
        从mongodb中初步筛选数据
        """
        # 获取所有信息
        data_info = self.collection.find({}, {'_id': 0, 'film_bref':0})
        # 将数据存入数据表中
        # print(list(data_info))
        # frame = pd.DataFrame(data=list(data_info))
        # print(frame.head())
        # for info in data_info:
        #     print(info)
        data_info = list(data_info)
        print(data_info)
        return data_info


if __name__ == '__main__':
    client = MongoDb('spider_info', 'film')
    data_info = client.query()
    import json
    with open('a.json', 'wb') as f:
        f.write(json.dumps(data_info, ensure_ascii=False).encode())
