from django.db import models
from django.contrib.auth.models import User

class ImageFeed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')
    processed_image = models.ImageField(upload_to='processed_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

