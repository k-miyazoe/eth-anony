# Generated by Django 3.1 on 2022-10-13 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20221013_0724'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='question_group',
            field=models.BooleanField(null=True),
        ),
    ]
