# Generated by Django 4.1.5 on 2023-02-03 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0007_employeeworkinghours_branchworkinghour'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branchworkinghour',
            name='end',
        ),
        migrations.RemoveField(
            model_name='branchworkinghour',
            name='start',
        ),
        migrations.AddField(
            model_name='branchworkinghour',
            name='workingHours',
            field=models.CharField(blank=True, default='000000000000000000000000', max_length=24),
        ),
    ]
