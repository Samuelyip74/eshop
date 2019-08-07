# Generated by Django 2.2.3 on 2019-08-07 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20190806_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='discountedprice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
    ]