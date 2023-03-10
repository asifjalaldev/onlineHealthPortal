# Generated by Django 4.1.1 on 2022-12-26 10:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Doctor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientName', models.CharField(default=None, max_length=50, null=True)),
                ('DOB', models.DateField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PatientCondition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptoms', models.TextField()),
                ('BP', models.CharField(blank=True, max_length=50)),
                ('BMI', models.CharField(blank=True, max_length=50)),
                ('BS', models.CharField(blank=True, max_length=50)),
                ('HB', models.CharField(blank=True, max_length=50)),
                ('platelets', models.CharField(blank=True, max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TestReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_path', models.CharField(max_length=100)),
                ('prescription_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Doctor.prescription')),
            ],
        ),
    ]
