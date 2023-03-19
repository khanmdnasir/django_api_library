import uuid
from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


class IssueTypesModel(models.Model):
    unique_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False)
    name = models.CharField(max_length=256, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING,related_name="issue_type_created_by",blank=False,null=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING,related_name="issue_type_updated_by",blank=True,null=True)

    class Meta:
        ordering = ["-id"]
    
    def __str__(self):
        return self.name



class TicketModel(models.Model):
    statusType = [('pending', 'pending'),
                ('assigned', 'assigned'),
                ('re-assigned', 're-assigned'),
                ('processing', 'processing'),
                ('completed', 'completed'),
                ('delivered', 'delivered'),
                ('rejected', 'rejected')
                ]

    priority = [('low', 'low'),
                ('medium', 'medium'),
                ('high', 'high'),
                ('critical', 'critical')
                ]

    unique_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False)
    title = models.CharField(max_length=256)
    issue_type = models.ForeignKey(
        IssueTypesModel, on_delete=models.DO_NOTHING, related_name='ticket', null=False, blank=False)
    phone = PhoneNumberField(unique=False, null=True, blank=True)
    email = models.EmailField(
        max_length=256, unique=False)
    description = models.TextField(
        max_length=512)

    is_open = models.BooleanField(default=True)

    status = models.CharField(
        max_length=64, choices=statusType)

    is_registered_user = models.BooleanField(default=False)

    support_agent =  models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='ticket_support_agent', blank=True, null=True, default=None)

    priority = models.CharField(
        max_length=64, choices=priority, null=True, blank=True)

    due_date = models.DateField(null=True, blank=True)


    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='ticket_approved_by', blank=True, null=True, default=None)

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-id"]
        permissions = (
            ("can_assign_support_agent","Can Assign Support Agent"),
            ("can_change_ticket_status","Can Change Ticket Status"),
            ("can_change_ticket_priority","Can Change Ticket Priority"),
            ("can_change_ticket_due_date","Can Change Ticket Due Date"),
            ("can_close_ticket","Can Close Ticket"),
            ("can_open_closed_ticket","Can Open Closed Ticket"),
            ("can_delete_ticket","Can Delete Ticket"),

            ("can_reply_ticket_comments","Can Reply Ticket Comments"),
        )

    def __str__(self):
        return self.title + ", Status: " + ("open" if self.is_open else "close")



class TicketCommentsModel(models.Model):
    unique_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False)
    ticket_id = models.ForeignKey(
        TicketModel, on_delete=models.CASCADE, related_name="ticket_comments")

    comment = models.CharField(max_length=256)

    is_customer = models.BooleanField(default=True)

    author =  models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='ticket_comments_author')

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.DO_NOTHING,related_name="ticket_comments_updated_by",blank=True,null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return str(("Ticket: " + self.ticket_id.title[:20] if len(self.ticket_id.title) > 20 else self.ticket_id.title) + ("commented by: " + self.comment[:20] if len(self.comment) > 20 else ", comment: " + self.comment))



class TicketLogsModel(models.Model):

    actionTypes = [('created', 'created'),
                ('updated', 'updated'),
                ('deleted', 'deleted'),
                ('close_ticket', 'close_ticket'),
                ('open_ticket', 'open_ticket'),
                ]

    unique_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False)
    ticket_id = models.ForeignKey(
        TicketModel, on_delete=models.CASCADE, related_name="ticket_logs")

    support_agent =  models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='ticket_logs_support_agent', blank=True, null=True, default=None)

    action_types = models.CharField(
        max_length=64, choices=actionTypes)
    
    details = models.TextField(
        max_length=512, null=True, blank=True)
    
    ticket_status = models.CharField(max_length=256)
    ticket_priority = models.CharField(max_length=256, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    action_creators_email = models.EmailField(
        max_length=256)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return ("Ticket: " + self.ticket_id.title[:20] if len(self.ticket_id.title) > 20 else self.ticket_id.title) + ", Ticket Status: " + self.ticket_status