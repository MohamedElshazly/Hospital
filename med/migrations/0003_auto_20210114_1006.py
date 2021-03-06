# Generated by Django 3.1.5 on 2021-01-14 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med', '0002_equipment_hospital'),
    ]

    operations = [
        migrations.AddField(
            model_name='engineer',
            name='orders_done',
            field=models.IntegerField(default=0, verbose_name='Total Work Orders Done'),
        ),
        migrations.AddField(
            model_name='engineer',
            name='response_time',
            field=models.DurationField(null=True, verbose_name='Response Time'),
        ),
        migrations.AddField(
            model_name='engineer',
            name='start_time',
            field=models.DurationField(null=True),
        ),
        migrations.AddField(
            model_name='engineer',
            name='total_orders',
            field=models.IntegerField(default=0, verbose_name='Total Work Orders'),
        ),
    ]
