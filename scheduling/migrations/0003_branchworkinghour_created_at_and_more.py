# Generated by Django 4.1.7 on 2023-03-26 14:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0002_alter_branchworkinghour_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='branchworkinghour',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='branchworkinghour',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='employeeworkinghour',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employeeworkinghour',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='branchworkinghour',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='employeeworkinghour',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]