# Generated by Django 2.0.5 on 2018-05-24 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20180524_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(max_length=20, verbose_name='账号'),
        ),
    ]
