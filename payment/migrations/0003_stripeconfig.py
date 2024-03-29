# Generated by Django 4.0.4 on 2023-03-02 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_eblconfig'),
    ]

    operations = [
        migrations.CreateModel(
            name='StripeConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_api_key', models.CharField(max_length=500)),
                ('stripe_access_key', models.CharField(max_length=500)),
                ('test_stripe_api_key', models.CharField(max_length=500)),
                ('test_stripe_access_key', models.CharField(max_length=500)),
                ('testMode', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
