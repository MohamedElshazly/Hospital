# Generated by Django 3.1.5 on 2021-01-14 09:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('med', '0004_auto_20210114_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='engineer',
            name='average_response_time',
            field=models.DurationField(default=datetime.timedelta(0), verbose_name='Average_Response Time'),
        ),
    ]