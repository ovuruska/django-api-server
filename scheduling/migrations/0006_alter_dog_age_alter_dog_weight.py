# Generated by Django 4.1.7 on 2023-03-03 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0005_alter_customer_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='age',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='dog',
            name='weight',
            field=models.FloatField(blank=True),
        ),
    ]