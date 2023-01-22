# Generated by Django 4.1.5 on 2023-01-22 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0004_remove_appointment_last_customer_appointment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Rescheduling', 'Rescheduling'), ('CheckedIn', 'Checked In'), ('PickupReady', 'Pickup Ready'), ('NoShow', 'No Show'), ('ClosedCharged', 'Closed Charge')], default='Pending', max_length=20),
        ),
    ]