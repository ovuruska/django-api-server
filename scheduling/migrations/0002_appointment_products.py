# Generated by Django 4.0.8 on 2022-12-05 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='products',
            field=models.ManyToManyField(related_name='products+', to='scheduling.product'),
        ),
    ]
