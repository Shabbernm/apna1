# Generated by Django 2.2.6 on 2020-03-30 23:33

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20200330_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcategory',
            name='image',
            field=models.ImageField(default='pics_default/default_shop_category.png', upload_to=core.models.shop_category_image_file_path),
        ),
    ]
