# Generated by Django 4.1.1 on 2023-01-02 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_appointment_time_alter_appointment_appointment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
