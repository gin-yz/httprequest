import json
import os
import sys
import django
import redis
sys.path.append(r'E:\PycharmProjects\httprequest')

os.chdir(r'E:\PycharmProjects\httprequest')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "httprequest.settings")
django.setup()

from apps import tasks
from apps.models import RedisQueue
uploadQueue = RedisQueue('upload','queue',host='127.0.0.1', port=6379,db=14,decode_responses=True)
workQueue = RedisQueue('work','queue',host='127.0.0.1', port=6379,db=14,decode_responses=True)

POOL = redis.ConnectionPool(host='127.0.0.1', port=6379,db=14,decode_responses=True)
while True:
    try:
        upload = uploadQueue.get_wait()
        work = workQueue.get_wait()
        json_result = json.loads(upload[1])
        if json_result['type'] == 1:
            tasks.uploadTask.delay(json_result['data'],work[1])
        if json_result['type'] == 2:
            tasks.informBlockChain.delay(json_result['data'],json_result['status'],work[1])
    except Exception as e:
        print(e)
        continue
    finally:
        continue


