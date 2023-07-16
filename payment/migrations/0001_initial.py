# Generated by Django 4.1.7 on 2023-05-11 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("scheduling", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CreditCard",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("exp_month", models.CharField(max_length=2)),
                ("exp_year", models.CharField(max_length=4)),
                ("first6", models.CharField(max_length=6)),
                ("last4", models.CharField(max_length=4)),
                ("brand", models.CharField(max_length=20)),
                ("token", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="credit_cards",
                        to="scheduling.customer",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]