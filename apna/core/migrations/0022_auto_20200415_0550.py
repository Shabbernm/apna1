# Generated by Django 2.2.6 on 2020-04-15 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20200415_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='MaximumOrder',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='shop',
            name='MinimumOrder',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
