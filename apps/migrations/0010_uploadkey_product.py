# Generated by Django 2.2.7 on 2020-04-12 22:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0009_uploadkey_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadkey',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='apps.ReceiveKey', verbose_name='购买的版权'),
        ),
    ]
