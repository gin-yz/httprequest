# Generated by Django 2.2.7 on 2020-04-22 11:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0022_uploadkey_productid'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceiveKey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('productId', models.CharField(max_length=128, verbose_name='版权上链id')),
                ('hash_result', models.CharField(max_length=42, verbose_name='交易成功hash')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
