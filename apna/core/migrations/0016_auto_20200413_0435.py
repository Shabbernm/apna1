# Generated by Django 2.2.6 on 2020-04-12 23:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_remove_profile_shop_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='User_Type',
        ),
        migrations.DeleteModel(
            name='UserType',
        ),
    ]
