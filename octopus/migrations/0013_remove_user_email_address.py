# Generated by Django 3.2.5 on 2021-10-23 06:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('octopus', '0012_rename_email_adress_user_email_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email_address',
        ),
    ]
