import os
import sys
import django

sys.path.append(r'E:\PycharmProjects\httprequest')

os.chdir(r'E:\PycharmProjects\httprequest')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "httprequest.settings")
django.setup()

import keyring
import asyncio
import ssl
import socket
import json
from apps.tasks import recivekeyTask, uploadkeyTask, modifyStatusTask
from utils.web3_module import init_web3
from utils.redis_module import init_redis

action = init_web3().get_web3()
init_redis()


async def handle_request(reader, writer):
    data = await reader.read(2048)
    print(data)
    addr = writer.get_extra_info('peername')
    print(f"Received task from {addr!r}")
    msg = json.loads(data.decode())
    send_msg = {'status': 'no'}
    if msg['type'] == 2:
        uploadkeyTask.delay(msg)
        send_msg['status'] = 'ok'

    if msg['type'] == 1:
        recivekeyTask.delay(msg)
        send_msg['status'] = 'ok'

    if msg['type'] ==3:
        modifyStatusTask.delay(msg)
        send_msg['status'] = 'ok'


    send_data = json.dumps(send_msg)

    writer.write(send_data.encode())
    await writer.drain()

    print(f"finsh {addr!r} work")
    writer.close()


async def main(sock, context):
    server = await asyncio.start_server(
        handle_request, sock=sock, ssl=context)

    print(f'Serving on {server.sockets}')

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    server_sock.bind(('127.0.0.1', 6666))
    server_sock.listen(5)
    server_sock.setblocking(False)
    path = os.getcwd().replace('/', '\\')
    CA_FILE = path + "\\utils\\ca.crt"
    KEY_FILE = path + "\\utils\\server.key"
    CERT_FILE = path + "\\utils\\server.crt"
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
    context.load_verify_locations(CA_FILE)
    context.verify_mode = ssl.CERT_REQUIRED
    asyncio.run(main(server_sock, context))
