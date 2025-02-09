# Generated by Django 5.0.6 on 2024-06-06 16:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("CoffeeSite", "0002_users_orders_orders_orderid_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="users_orders",
            name="Orders_orderID",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="CoffeeSite.orders",
            ),
        ),
        migrations.AlterField(
            model_name="users_orders",
            name="Users_username",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="users_orders",
            unique_together={("Users_username", "Orders_orderID")},
        ),
    ]
