# Generated by Django 2.2.7 on 2020-04-12 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0007_auto_20200412_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadkey',
            name='transactionHash',
            field=models.CharField(default='', max_length=128, verbose_name='交易hash'),
        ),
    ]
