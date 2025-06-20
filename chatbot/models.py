from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField

class Product(models.Model):
    sku         = models.CharField(max_length=50, unique=True)
    name        = models.CharField(max_length=200)
    description = models.TextField()
    sizes       = ArrayField(models.CharField(max_length=5))
    price       = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    session_id  = models.CharField(max_length=100, unique=True)
    height_cm   = models.PositiveIntegerField(null=True, blank=True)
    weight_kg   = models.PositiveIntegerField(null=True, blank=True)
    body_type   = models.CharField(max_length=50, blank=True)
    past_orders = ArrayField(models.CharField(max_length=50), default=list, blank=True)

    def __str__(self):
        return f"Profile {self.session_id}"

class ChatMessage(models.Model):
    session     = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="messages")
    role        = models.CharField(max_length=10, choices=[('user','user'),('assistant','assistant')])
    content     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']
