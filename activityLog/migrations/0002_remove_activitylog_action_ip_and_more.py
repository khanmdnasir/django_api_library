# Generated by Django 4.0.4 on 2023-01-19 11:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activityLog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activitylog',
            name='action_IP',
        ),
        migrations.RemoveField(
            model_name='activitylog',
            name='action_agent_info',
        ),
    ]