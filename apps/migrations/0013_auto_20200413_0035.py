# Generated by Django 2.2.7 on 2020-04-13 00:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0012_auto_20200412_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadkey',
            name='address',
            field=models.CharField(default='', max_length=42, verbose_name='账户地址'),
        ),
    ]
