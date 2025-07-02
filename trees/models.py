from django.db import models

class Tree(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    plantId = models.CharField(max_length=20, null=True, blank=True)
    desc = models.TextField(max_length=400, null=True, blank=True)
    type = models.CharField(max_length=20, null=True, blank=True)
    fieldName = models.CharField(max_length=20, null=True, blank=True)
    lineNumber = models.CharField(max_length=20, null=True, blank=True)
    plantNumber = models.CharField(max_length=20, null=True, blank=True)
    imageUrl = models.ImageField(upload_to='trees/images/', null=True, blank=True)

    def __str__(self):
        return self.name or "Unnamed Tree"
