# Generated by Django 5.1.1 on 2024-09-30 14:52

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('psychoshield', '0004_user_last_login'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='pbkdf2_sha256$870000$oGYWxVbqW22xS9Naik5v3w$tRjdrd1JYT/nANMsyf9H7bdq1Rhj15CY4Oz5/E33oQ4=', max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
