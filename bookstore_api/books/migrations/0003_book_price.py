# Generated by Django 4.2.9 on 2024-01-25 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_shoppingcart_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, default=100, max_digits=10),
            preserve_default=False,
        ),
    ]
