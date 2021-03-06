# Generated by Django 2.2.6 on 2020-04-11 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200408_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='shopproduct',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='shopproductcategory',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=255, null=True),
        ),
    ]
