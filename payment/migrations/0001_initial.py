# Generated by Django 4.0.4 on 2023-02-20 05:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prefix', models.CharField(blank=True, max_length=10, null=True)),
                ('short_key', models.CharField(max_length=100, unique=True)),
                ('rate', models.DecimalField(decimal_places=5, default=0, max_digits=8)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentGatewayModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payment.currencymodel')),
            ],
        ),
    ]
