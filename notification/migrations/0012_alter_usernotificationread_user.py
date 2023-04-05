# Generated by Django 4.1.7 on 2023-03-27 06:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notification', '0011_notificationmodel_is_onetime_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernotificationread',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
