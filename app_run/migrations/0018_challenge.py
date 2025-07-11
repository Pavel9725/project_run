# Generated by Django 5.2 on 2025-06-29 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_run', '0017_alter_athleteinfo_weight'),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255)),
                ('athlete', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenges', to='app_run.athleteinfo')),
            ],
        ),
    ]
