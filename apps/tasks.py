from __future__ import absolute_import, unicode_literals

import time
from tempfile import TemporaryFile

import keyring
import ipfshttpclient
import json
from celery import shared_task
from celery.result import AsyncResult, allow_join_result

from apps.models import RedisQueue, UploadKey, Key_db_one, Key_db_two, Key_db_three, Key_db_four, \
    Key_db_five, ReceiveKey
from ecies import encrypt, decrypt
from random import sample
from apps.views import loadcontact
from web3 import Web3
from binascii import b2a_hex, a2b_hex
from httprequest.settings import BASE_DIR
from utils.ssl_client import client_ssl

uploadQueue = RedisQueue('upload', 'queue', host='127.0.0.1', port=6379, db=14, decode_responses=True)
workQueue = RedisQueue('work', 'queue', host='127.0.0.1', port=6379, db=14, decode_responses=True)
client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')
w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
action = loadcontact(w3, 'cys')

# @shared_task
# def call_mainsystem(purchase_bcId, ipfshash):
#     request_data = {
#         'purchase_bcId': str(purchase_bcId),
#         'ipfshash': str(ipfshash),
#     }
#     r0 = requests.post('http://127.0.0.1:8000/receiveuploadsystem/', data=request_data)
#     if r0.text == 'ok':
#         uploadkey = UploadKey.objects.filter(purchase_bcId=str(purchase_bcId))
#         if uploadkey:
#             uploadkey = uploadkey.first()
#             uploadkey.status = 2
#             uploadkey.save()
#             return "inform main system success"
#     else:
#         return "inform main system fail"
list_select = [1, 2, 3, 4, 5]
client_one = client_ssl(7777)
client_two = client_ssl(7778)
client_three = client_ssl(7779)
client_four = client_ssl(7780)
client_five = client_ssl(7781)
switch = {
    1: client_one,
    2: client_two,
    3: client_three,
    4: client_four,
    5: client_five,
}


@shared_task()
def find_single_key(type, msg):
    return switch.get(type).send_msg(msg)


def find_shamir_key(id, public):
    msg = {
        "productId": id,
        "public": public,
    }
    task_list = locals()
    for num, x in enumerate(sample(list_select, 3)):
        task_list['task%s' % num] = AsyncResult(id=find_single_key.delay(x, msg).id)

    while not (task_list['task0'].ready() & task_list['task1'].ready() & task_list['task2'].ready()):
        # print(task_list['task0'].ready(),task_list['task1'].ready(),task_list['task2'].ready())
        pass
    # key_list = [switch.get(x).send_msg(msg) for x in sample(list_select,3)]
    with allow_join_result():
        return '%s,%s,%s' % (task_list['task0'].get(), task_list['task1'].get(), task_list['task2'].get())


@shared_task
def uploadTask(upload, work):
    uploadkey = UploadKey.objects.filter(id=int(upload))
    if not uploadkey:
        return "DB not key"
    uploadkey = uploadkey.first()
    key_data = find_shamir_key(uploadkey.productId, str(uploadkey.public))
    # uploadfinal = encrypt(str(uploadkey.public), key_data.encode())
    ipfshash = client.add_bytes(key_data.encode())
    address = 'address' + str(work)
    private = 'private' + str(work)
    nonce = w3.eth.getTransactionCount(keyring.get_password("DRMDEMO", address))
    txn_dict = action.functions.uploadLicense(int(uploadkey.purchase_bcId), ipfshash).buildTransaction({
        'nonce': nonce,
        "from": keyring.get_password("DRMDEMO", address),
    })
    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=keyring.get_password('DRMDEMO', private))
    result_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    uploadkey.key_ipfsHash = ipfshash
    uploadkey.transactionHash = w3.toHex(result_hash)
    uploadkey.status = 1
    uploadkey.save()
    workQueue.put(work)
    # call_mainsystem.delay(uploadkey.purchase_bcId, ipfshash)
    return "upload key success"


@shared_task
def saveDbOneTask(id, msg):
    try:
        key_db_one = Key_db_one.objects.using('shamir_key_one').create()
        key_db_one.productId = id
        key_db_one.key = msg
        key_db_one.save()
    except Exception as e:
        return e
    return 'save one db success'


@shared_task
def saveDbTwoTask(id, msg):
    try:
        key_db_two = Key_db_two.objects.using('shamir_key_two').create()
        key_db_two.productId = id
        key_db_two.key = msg
        key_db_two.save()
    except Exception as e:
        return e
    return 'save two db success'


@shared_task
def saveDbThreeTask(id, msg):
    try:
        key_db_three = Key_db_three.objects.using('shamir_key_tree').create()
        key_db_three.productId = id
        key_db_three.key = msg
        key_db_three.save()
    except Exception as e:
        return e
    return 'save three db success'


@shared_task
def saveDbFourTask(id, msg):
    try:
        key_db_four = Key_db_four.objects.using('shamir_key_four').create()
        key_db_four.productId = id
        key_db_four.key = msg
        key_db_four.save()
    except Exception as e:
        return e
    return 'save four db success'


@shared_task
def saveDbFiveTask(id, msg):
    try:
        key_db_five = Key_db_five.objects.using('shamir_key_five').create()
        key_db_five.productId = id
        key_db_five.key = msg
        key_db_five.save()
    except Exception as e:
        return e
    return 'save five db success'


@shared_task
def recivekeyTask(msg):
    try:
        # list = decrypt(keyring.get_password("DRMDEMO", 'private'), a2b_hex(msg['keyfile'])).decode().split(',')
        list = msg['keyfile'].split(',')
        # print(list)
    except Exception as e:
        return e
    try:
        one = AsyncResult(id=saveDbOneTask.delay(msg['productId'], list[0]).id)
        two = AsyncResult(id=saveDbTwoTask.delay(msg['productId'], list[1]).id)
        three = AsyncResult(id=saveDbThreeTask.delay(msg['productId'], list[2]).id)
        four = AsyncResult(id=saveDbFourTask.delay(msg['productId'], list[3]).id)
        five = AsyncResult(id=saveDbFiveTask.delay(msg['productId'], list[4]).id)
        while True:
            if one.successful() & two.successful() & three.successful() & four.successful() & five.successful():
                break
    except Exception as e:
        return e
    msg = {
        'type': 2,
        'status': msg['status'],
        'data': int(msg['productId'])
    }
    json_msg = json.dumps(msg)
    try:
        uploadQueue.put(json_msg)
    except Exception as e:
        return e
    return 'allot save db success'


@shared_task
def informBlockChain(productId,status, work):
    address = 'address' + str(work)
    private = 'private' + str(work)
    nonce = w3.eth.getTransactionCount(keyring.get_password("DRMDEMO", address))
    txn_dict = action.functions.modifyProductAdmin(int(productId), status).buildTransaction({
        'nonce': nonce,
        "from": keyring.get_password("DRMDEMO", address),
    })
    signed_txn = w3.eth.account.signTransaction(txn_dict, private_key=keyring.get_password('DRMDEMO', private))
    result_hash = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
    receive = ReceiveKey.objects.filter(productId=int(productId))
    if receive:
        receive = receive.first()
    else:
        receive = ReceiveKey()
    receive.productId = productId
    receive.hash_result = result_hash.hex()
    receive.save()
    workQueue.put(work)
    return 'inform CopyRight %s success' % productId


@shared_task
def uploadkeyTask(msg):
    # print(msg)
    uploadkey = UploadKey.objects.filter(purchase_bcId=str(msg['purchase_bcId']))
    if not uploadkey:
        uploadkey = UploadKey()
    else:
        uploadkey = uploadkey.last()
    uploadkey.address = msg['address']
    uploadkey.productId = msg['productId']
    uploadkey.purchase_bcId = msg['purchase_bcId']
    uploadkey.public = msg['public']
    uploadkey.save()
    msg = {
        'type': 1,
        'data': uploadkey.id
    }
    json_msg = json.dumps(msg)
    try:
        uploadQueue.put(json_msg)
    except Exception as e:
        return e
    return 'upload buy key Task success'


@shared_task
def modifyStatusTask(msg):
    msg = {
        'type': 2,
        'status': msg['status'],
        'data': int(msg['productId'])
    }
    json_msg = json.dumps(msg)
    try:
        uploadQueue.put(json_msg)
    except Exception as e:
        return e
    return 'allot save db success'