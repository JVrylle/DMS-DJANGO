# Generated by Django 5.1.7 on 2025-05-22 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dental', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled'), ('No Show', 'No Show'), ('Pending-Walk-in', 'Pending-Walk-in')], db_index=True, default='Scheduled', max_length=20),
        ),
    ]
