# Generated by Django 2.2.7 on 2020-04-22 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0023_receivekey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receivekey',
            name='hash_result',
            field=models.CharField(max_length=128, verbose_name='交易成功hash'),
        ),
    ]
