# Generated by Django 5.2 on 2025-06-29 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_run', '0011_alter_athleteinfo_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='athleteinfo',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
    ]
