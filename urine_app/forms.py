from django import forms
from .models import *

class UrineImageForm(forms.ModelForm):
    class Meta:
        model = UrineImage
        fields = ['image']