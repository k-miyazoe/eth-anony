# Generated by Django 3.1 on 2022-10-12 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20221012_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='answer_eth_address',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='question',
            name='question_eth_address',
            field=models.CharField(default='', max_length=50),
        ),
    ]
