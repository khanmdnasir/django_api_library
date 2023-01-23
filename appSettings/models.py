from django.db import models
from solo.models import SingletonModel

# Create your models here.
storage_choices = (

    ('local','local'),
    ('aws','aws'),
    ('gcp','gcp')
)
class AppSettings(SingletonModel):
    debug = models.BooleanField(default=True)
    storage_used = models.CharField(max_length=50,choices=storage_choices,default='local')
    

class DocumentModel(models.Model):
    file = models.FileField(upload_to='document/%Y/%m/%d')


