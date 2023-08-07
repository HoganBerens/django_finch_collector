from django.db import models


# Create your models here.
class Finch(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.id})"
