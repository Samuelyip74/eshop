# Generated by Django 2.2.3 on 2019-08-04 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20190704_1504'),
        ('carts', '0004_auto_20190804_2105'),
    ]

    operations = [
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.ForeignKey(on_delete='CASCADE', to='products.Product')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='item',
            field=models.ManyToManyField(to='carts.CartItem'),
        ),
    ]