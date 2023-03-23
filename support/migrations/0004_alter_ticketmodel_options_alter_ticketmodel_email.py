# Generated by Django 4.0.4 on 2023-03-19 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0003_alter_ticketcommentsmodel_is_customer'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticketmodel',
            options={'ordering': ['-id'], 'permissions': (('can_assign_support_agent', 'Can Assign Support Agent'), ('can_change_ticket_status', 'Can Change Ticket Status'), ('can_change_ticket_priority', 'Can Change Ticket Priority'), ('can_change_ticket_due_date', 'Can Change Ticket Due Date'), ('can_close_ticket', 'Can Close Ticket'), ('can_open_closed_ticket', 'Can Open Closed Ticket'), ('can_delete_ticket', 'Can Delete Ticket'), ('can_reply_ticket_comments', 'Can Reply Ticket Comments'))},
        ),
        migrations.AlterField(
            model_name='ticketmodel',
            name='email',
            field=models.EmailField(max_length=256),
        ),
    ]