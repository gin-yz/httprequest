import os
import sys
import django
import redis
sys.path.append(r'E:\PycharmProjects\httprequest')

os.chdir(r'E:\PycharmProjects\httprequest')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "httprequest.settings")
django.setup()


# from apps.models import ReceiveKey
from httprequest.settings import BASE_DIR
# print(ReceiveKey.objects.get(id =26).keyfile.read())