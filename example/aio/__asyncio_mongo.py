"""
通过 asyncio （协程）应用 PyMongo
"""
import asyncio

from pymongo import MongoClient


class AsyncMongoClient(MongoClient):
    """
    协程版MongoClient实现
    """

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()


async def mongo_testing():
    async with AsyncMongoClient(host="mongo.zlikun.com", port=27017) as client:
        db = client.example

        # 写入一条数据
        result = db.user.insert_one({"name": "zlikun", "gender": "MALE"})
        # <class 'bson.objectid.ObjectId'> 5baf522ca6c85b326c86b3b2
        print(type(result.inserted_id), result.inserted_id)

        # 查询这条数据
        data = db.user.find_one({"_id": result.inserted_id})
        # {'_id': ObjectId('5baf522ca6c85b326c86b3b2'), 'name': 'zlikun', 'gender': 'MALE'}
        print(data)


if __name__ == '__main__':
    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(mongo_testing())
    finally:
        event_loop.close()
