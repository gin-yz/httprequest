import redis

class RedisQueue(object):
    def __init__(self, name, namespace='queue', **redis_kwargs):
        self.__db = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def qsize(self):
        return self.__db.llen(self.key)  # 返回队列里面list内元素的数量

    def put(self, value):
        self.__db.rpush(self.key,value)  # 添加新元素到队列最右方

    def get_wait(self, timeout=None):
        # 返回队列第一个元素，如果为空则等待至有元素被加入队列（超时时间阈值为timeout，如果为None则一直等待）
        item = self.__db.blpop(self.key, timeout=timeout)
        # if item:
        #     item = item[1]  # 返回值为一个tuple
        return item

    def get_nowait(self):
        # 直接返回队列第一个元素，如果队列为空返回的是None
        item = self.__db.lpop(self.key)
        return item

    def flush_db(self):
        self.__db.flushdb()

class init_redis(object):
    def __init__(self):
        self.uploadQueue = RedisQueue('upload', 'queue', host='127.0.0.1', port=6379, db=14, decode_responses=True)
        self.workQueue = RedisQueue('work', 'queue', host='127.0.0.1', port=6379, db=14, decode_responses=True)
        self.workQueue.flush_db()
        for i in range(3):
            self.workQueue.put(i + 1)