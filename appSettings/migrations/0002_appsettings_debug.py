# Generated by Django 4.0.4 on 2023-01-23 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appSettings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='appsettings',
            name='debug',
            field=models.BooleanField(default=True),
        ),
    ]
