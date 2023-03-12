# Generated by Django 4.1.7 on 2023-03-07 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_alter_ordermodel_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='status',
            field=models.CharField(choices=[('processing', 'Processing'), ('success', 'Success'), ('cancelled', 'Cancelled'), ('failed', 'Failed')], default='Processing', max_length=50),
        ),
    ]
