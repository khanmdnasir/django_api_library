# Generated by Django 4.0.4 on 2023-02-08 05:01

import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0003_smsconfigmodel_alter_emailschedulemodel_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailschedulemodel',
            options={},
        ),
        migrations.AlterModelOptions(
            name='notificationmodel',
            options={},
        ),
        migrations.AlterModelOptions(
            name='smsschedulemodel',
            options={},
        ),
        migrations.RemoveField(
            model_name='emailschedulemodel',
            name='sent',
        ),
        migrations.RemoveField(
            model_name='notificationmodel',
            name='broadcast_on',
        ),
        migrations.RemoveField(
            model_name='smsschedulemodel',
            name='sent',
        ),
        migrations.AddField(
            model_name='emailschedulemodel',
            name='schedule_day',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)]),
        ),
        migrations.AddField(
            model_name='emailschedulemodel',
            name='schedule_month',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
        ),
        migrations.AddField(
            model_name='notificationmodel',
            name='broadcast_day',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)]),
        ),
        migrations.AddField(
            model_name='notificationmodel',
            name='broadcast_month',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
        ),
        migrations.AddField(
            model_name='notificationmodel',
            name='broadcast_time',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='smsschedulemodel',
            name='schedule_day',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)]),
        ),
        migrations.AddField(
            model_name='smsschedulemodel',
            name='schedule_month',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)]),
        ),
        migrations.AlterField(
            model_name='emailschedulemodel',
            name='schedule_time',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='smsschedulemodel',
            name='schedule_time',
            field=models.TimeField(),
        ),
    ]