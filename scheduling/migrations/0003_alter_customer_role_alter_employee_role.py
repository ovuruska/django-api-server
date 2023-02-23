

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduling', '0002_customer_role_alter_employee_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (10, 10), (15, 15), (20, 20), (30, 30), (40, 40)], default=1),
        ),
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 1), (10, 10), (15, 15), (20, 20), (30, 30), (40, 40)], default=10),
        ),
    ]