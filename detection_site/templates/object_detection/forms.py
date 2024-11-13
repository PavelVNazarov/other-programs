from django import forms
from .models import ImageFeed

class ImageFeedForm(forms.ModelForm):
    class Meta:
        model = ImageFeed
        fields = ['image']  # Указываем, какие поля будут в форме