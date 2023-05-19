# Generated by Django 4.1.7 on 2023-05-11 05:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="creditcard",
            old_name="token",
            new_name="card_token",
        ),
        migrations.AddField(
            model_name="creditcard",
            name="customer_token",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
