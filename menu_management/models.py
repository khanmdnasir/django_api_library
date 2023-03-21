from django.db import models
from user.models import User

# Create your models here.
class Menu(models.Model):
    name = models.CharField(max_length=255,unique=True)
    icon = models.FileField(upload_to='images/icons/',null=True)
    url = models.CharField(max_length=500)
    users = models.ManyToManyField(User)
    active = models.BooleanField(default=True)
    serial = models.PositiveIntegerField(unique=True)

    def __str__(self):
        return self.name

class SubMenu(models.Model):
    name = models.CharField(max_length=255,unique=True)
    icon = models.FileField(upload_to='images/icons/',null=True)
    url = models.CharField(max_length=500)
    menu = models.ForeignKey(Menu,on_delete=models.CASCADE)
    users = models.ManyToManyField(User)
    active = models.BooleanField(default=True)
    serial = models.PositiveIntegerField()

    class Meta:
        unique_together=(('menu','serial'),)

    def __str__(self):
        return self.name