# Generated by Django 2.2.3 on 2019-08-04 13:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_auto_20190804_2051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='items',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
