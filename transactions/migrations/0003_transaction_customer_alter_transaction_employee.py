# Generated by Django 4.1.5 on 2023-02-28 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0003_alter_customer_role_alter_employee_role'),
        ('transactions', '0002_alter_transaction_employee'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='scheduling.customer'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='scheduling.employee'),
        ),
    ]
