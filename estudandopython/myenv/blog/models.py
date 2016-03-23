from django.db import models
from django.utils import timezone
from geoposition.fields import GeopositionField

# Create your models here.
class Post(models.Model):
    author=models.ForeignKey('auth.User')
    title=models.CharField(max_length=200,null=False,blank=False)
    text=models.TextField()
    created_date=models.DateTimeField(default=timezone.now)
    published_date=models.DateTimeField(blank=True,null=True)
    local=GeopositionField()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def _str_(self):
      return self.title