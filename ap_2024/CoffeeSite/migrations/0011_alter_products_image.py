# Generated by Django 5.0.6 on 2024-06-27 13:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("CoffeeSite", "0010_alter_orders_date_alter_products_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="products",
            name="image",
            field=models.ImageField(default=None, upload_to=""),
        ),
    ]
