# Generated by Django 4.1.5 on 2023-02-09 13:03

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, default='', max_length=256)),
                ('address', models.CharField(blank=True, default='', max_length=256)),
                ('description', models.CharField(blank=True, default='', max_length=256)),
                ('phone', models.CharField(blank=True, default='', max_length=32)),
                ('email', models.EmailField(blank=True, default='', max_length=254)),
                ('tubs', models.IntegerField(blank=True, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=64)),
                ('uid', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=32)),
                ('address', models.CharField(max_length=128)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=128)),
                ('phone', models.CharField(blank=True, max_length=16)),
                ('email', models.CharField(blank=True, max_length=64)),
                ('role', models.CharField(blank=True, choices=[('Full Grooming', 'Full Grooming'), ('We Wash', 'We Wash')], default='We Wash', max_length=16)),
                ('uid', models.CharField(blank=True, max_length=64)),
                ('branch', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='scheduling.branch')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Payroll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_name', models.CharField(max_length=128)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('tips', models.DecimalField(decimal_places=2, max_digits=10)),
                ('service_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_cost', models.DecimalField(decimal_places=2, max_digits=10)),
                ('working_hours', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('category', models.CharField(default='Other', max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=8)),
                ('duration', models.DurationField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=32)),
                ('breed', models.CharField(max_length=128)),
                ('age', models.IntegerField()),
                ('weight', models.FloatField()),
                ('description', models.TextField(default='', max_length=200)),
                ('rabies_vaccination', models.DateField()),
                ('employee_notes', models.TextField(default='', max_length=1000)),
                ('customer_notes', models.TextField(default='', max_length=1000)),
                ('special_handling', models.BooleanField(default=False)),
                ('coat_type', models.CharField(choices=[('SmoothShort', 'Smooth (Short)'), ('SmoothLong', 'Smooth (Long)'), ('DoubleCoated', 'Double Coated'), ('Doodles', 'Doodles')], default='SmoothLong', max_length=20)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dogs', to='scheduling.customer')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start', models.DateTimeField(default=django.utils.timezone.now)),
                ('end', models.DateTimeField(default=django.utils.timezone.now)),
                ('customer_notes', models.TextField(blank=True, max_length=1000)),
                ('employee_notes', models.TextField(blank=True, max_length=1000)),
                ('tip', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('Rescheduling', 'Rescheduling'), ('CheckedIn', 'Checked In'), ('PickUpReady', 'Pickup Ready'), ('NoShow', 'No Show'), ('ClosedCharged', 'Closed Charged')], default='Pending', max_length=20)),
                ('appointment_type', models.CharField(choices=[('Full Grooming', 'Full Grooming'), ('We Wash', 'We Wash')], default='We Wash', max_length=20)),
                ('reminder_sent', models.DateTimeField(blank=True, null=True)),
                ('check_in', models.DateTimeField(blank=True, null=True)),
                ('pick_up', models.DateTimeField(blank=True, null=True)),
                ('confirmed_on', models.DateTimeField(blank=True, null=True)),
                ('checkout_time', models.DateTimeField(blank=True, null=True)),
                ('checkout_status', models.BooleanField(default=False)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='scheduling.branch')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='appointments', to='scheduling.customer')),
                ('dog', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='appointments', to='scheduling.dog')),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='appointments', to='scheduling.employee')),
                ('products', models.ManyToManyField(blank=True, default=[], related_name='products+', to='scheduling.product')),
                ('services', models.ManyToManyField(blank=True, default=[], related_name='appointments', to='scheduling.service')),
            ],
            options={
                'ordering': ['-start'],
            },
        ),
        migrations.CreateModel(
            name='EmployeeWorkingHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_day', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(6)])),
                ('start', models.DateTimeField(null=True)),
                ('end', models.DateTimeField(null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduling.branch')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduling.employee')),
            ],
            options={
                'ordering': ('-start',),
                'unique_together': {('employee', 'start')},
            },
        ),
        migrations.CreateModel(
            name='BranchWorkingHour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('week_day', models.IntegerField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('start', models.DateTimeField(null=True)),
                ('end', models.DateTimeField(null=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scheduling.branch')),
            ],
            options={
                'unique_together': {('branch', 'date')},
            },
        ),
    ]
