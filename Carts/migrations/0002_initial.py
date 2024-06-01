# Generated by Django 5.0.2 on 2024-06-01 03:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Carts', '0001_initial'),
        ('Products', '0001_initial'),
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='Users.customuser'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='Carts.cart'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Products.product'),
        ),
        migrations.AddField(
            model_name='cart',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Carts.coupon'),
        ),
    ]
