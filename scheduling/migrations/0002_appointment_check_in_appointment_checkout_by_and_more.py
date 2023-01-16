# Generated by Django 4.1.5 on 2023-01-16 18:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='check_in',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='checkout_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='checkout_appointments', to='scheduling.employee'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='checkout_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='appointment',
            name='checkout_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='confirmed_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='pick_up',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='reminder_sent',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appointment',
            name='special_handling',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='branch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='scheduling.branch'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='dog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='appointments', to='scheduling.dog'),
        ),
    ]
