# Generated by Django 4.1 on 2022-09-16 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0005_alter_product_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_image_1',
            field=models.ImageField(upload_to='photos/product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image_2',
            field=models.ImageField(upload_to='photos/product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image_3',
            field=models.ImageField(upload_to='photos/product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_image_4',
            field=models.ImageField(upload_to='photos/product'),
        ),
    ]