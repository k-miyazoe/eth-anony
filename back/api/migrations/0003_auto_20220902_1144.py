# Generated by Django 3.1 on 2022-09-02 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20220829_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_group',
            field=models.NullBooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='user_point',
            field=models.IntegerField(default=0),
        ),
    ]
