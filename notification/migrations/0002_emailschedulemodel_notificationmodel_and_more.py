# Generated by Django 4.0.4 on 2023-02-05 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailScheduleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_time', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('schedule', 'schedule'), ('broadcast', 'broadcast'), ('non_schedule', 'non_schedule')], max_length=255)),
                ('message', models.TextField()),
                ('broadcast_on', models.DateTimeField(null=True)),
                ('sent', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-broadcast_on'],
            },
        ),
        migrations.CreateModel(
            name='SMSScheduleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_time', models.DateTimeField()),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.DeleteModel(
            name='InternalNotificationModel',
        ),
    ]