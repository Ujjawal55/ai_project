from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True, unique=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return str(self.name)
