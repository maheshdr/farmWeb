from django.db import models

class Tree(models.Model):
    PLANT_TYPE_CHOICES = [
        ('Wild', 'Wild'),
        ('Medicinal', 'Medicinal'),
        ('Fruit', 'Fruit'),
    ]

    FIELD_TYPE_CHOICES = [
        ('F1', 'F1'),
        ('F2', 'F2'),
        ('F3', 'F3'),
    ]

    plantName = models.CharField(max_length=100, default='NA')  # required
    plantId = models.CharField(max_length=20, unique=True)  # required
    description = models.TextField(max_length=400, null=True, blank=True)  # optional
    plantType = models.CharField(max_length=20, choices=PLANT_TYPE_CHOICES, default='Other')  # dropdown, optional
    fieldName = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES, default='F1')  # required
    lineNumber = models.CharField(max_length=20, default='1')  # required
    plantNumber = models.CharField(max_length=20, default='1')  # required
    imageUrl = models.ImageField(upload_to='trees/images/', null=True, blank=True)  # required

    def save(self, *args, **kwargs):
        if not self.plantId:
            last = Tree.objects.order_by('-id').first()
            next_id = 1 if not last else last.id + 1
            self.plantId = f"DM{next_id:03d}"  # e.g., DM001, DM002, ...
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
