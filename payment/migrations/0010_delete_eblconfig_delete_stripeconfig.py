# Generated by Django 4.1.7 on 2023-03-07 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0009_paymentgatewaymodel_access_key_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EBLConfig',
        ),
        migrations.DeleteModel(
            name='StripeConfig',
        ),
    ]
