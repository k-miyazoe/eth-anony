# Generated by Django 3.1 on 2022-09-22 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20220902_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_email',
            field=models.EmailField(default='', max_length=255, verbose_name='メールアドレス'),
        ),
    ]
