# Generated by Django 4.1.7 on 2023-05-16 05:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0003_alter_creditcard_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="creditcard",
            name="brand",
            field=models.CharField(max_length=32),
        ),
    ]
