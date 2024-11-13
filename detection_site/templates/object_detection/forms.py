from django import forms
from .models import ImageFeed

class ImageFeedForm(forms.ModelForm):
    class Meta:
        model = ImageFeed
        fields = ['image', 'description']  # Укажите поля, которые хотите включить в форму
