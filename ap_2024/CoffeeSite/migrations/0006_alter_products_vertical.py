# Generated by Django 5.0.6 on 2024-06-07 11:55

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("CoffeeSite", "0005_rename_products_orders_product_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="vertical",
            field=models.CharField(max_length=255),
        ),
    ]
