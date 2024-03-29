# Generated by Django 2.2.3 on 2019-07-07 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carts', '0002_cart_subtotal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=120)),
                ('status', models.CharField(choices=[('created', 'Created'), ('paid', 'Paid'), ('shipped', 'Shipped'), ('refunded', 'Refunded'), ('cancelled', 'Cancelled')], default='created', max_length=120)),
                ('shipping_total', models.DecimalField(decimal_places=2, default=10.0, max_digits=100)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=100)),
                ('cart', models.ForeignKey(on_delete='CASCADE', to='carts.Cart')),
            ],
        ),
    ]
