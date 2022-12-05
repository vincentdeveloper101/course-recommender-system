from django import forms

from .models import Rating


class AddRatingForm(forms.ModelForm):

    class Meta:
        model = Rating
        fields = ['rating']
        labels = {'rating': 'Rating'}
        widgets = {
            'rating': forms.TextInput(attrs={'type': 'range', 'step': '1', 'min': '0', 'max': '5', 'class': {'custom-range', 'border-0'}})
        }
