# Generated by Django 4.1.7 on 2023-03-13 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0011_alter_dog_coat_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dog',
            name='coat_type',
            field=models.CharField(default='SmoothLong', max_length=20),
        ),
    ]