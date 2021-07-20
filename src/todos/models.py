from django.db import models
from django.conf import settings

class Todo(models.Model):
    description = models.CharField(max_length=1000)
    created     = models.DateTimeField(editable=False, auto_now_add=True)
    modified    = models.DateTimeField(editable=False, auto_now=True)
    collection  = models.ForeignKey('Collection', on_delete=models.CASCADE, related_name="todos")
    done        = models.BooleanField(default=False)
    done        = models.BooleanField(default=False)


class Collection(models.Model):
    name        = models.CharField(max_length=200)
    created     = models.DateTimeField(editable=False, auto_now_add=True)
    modified    = models.DateTimeField(editable=False, auto_now=True)
    owner       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
      return f'{self.name} - {self.owner.email}'
