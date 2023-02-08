# Generated by Django 4.1.5 on 2023-02-08 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0005_alter_employeeworkinghour_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='branchworkinghour',
            name='working_hours',
        ),
        migrations.AddField(
            model_name='branchworkinghour',
            name='end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='branchworkinghour',
            name='start',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='employeeworkinghour',
            name='end',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='employeeworkinghour',
            name='start',
            field=models.DateTimeField(null=True),
        ),
    ]
