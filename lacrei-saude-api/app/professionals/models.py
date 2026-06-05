from django.db import models
import uuid


class Professional(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    social_name = models.CharField(max_length=255)
    profession = models.CharField(max_length=255)
    address = models.TextField()
    contact = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.social_name
