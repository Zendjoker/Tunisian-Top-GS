# Generated by Django 5.0.2 on 2024-06-26 02:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Courses', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateSessionRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_mode', models.CharField(blank=True, choices=[('0', 'a session by yourself alone'), ('1', 'a session just between you and your friends'), ('2', 'a session including you and another group')], max_length=20, null=True)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('duration_hours', models.PositiveIntegerField(blank=True, choices=[(30, '30 Minutes'), (60, '1 Hour'), (90, '1H 30 Minutes'), (120, '2 Hours')], null=True)),
                ('selected_professor', models.CharField(blank=True, choices=[(0, 'az'), (1, '1 zz'), (2, '1H 30zz Minutes')], max_length=150, null=True)),
                ('session_date', models.DateTimeField(blank=True, null=True)),
                ('additional_notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrivateSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='scheduled', max_length=20, null=True)),
                ('schedule', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('session_mode', models.IntegerField(choices=[(0, 'A session by yourself alone'), (1, 'A session just between you and your friends'), (2, 'A session including you and another group')], default=0)),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='private_sessions', to='Courses.course')),
            ],
        ),
    ]
