# Generated by Django 2.2.7 on 2020-03-19 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0005_uploadkey_transactionhash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadkey',
            name='transactionHash',
            field=models.CharField(max_length=128, verbose_name='交易hash'),
        ),
    ]
