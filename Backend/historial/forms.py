# backend/historial/forms.py
from django import forms
from .models import Club

class ClubForm(forms.ModelForm):
    fundacion = forms.IntegerField(
        min_value=1800,
        max_value=2023,
        help_text="Año de fundación del club"
    )
    
    class Meta:
        model = Club
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'localidad': forms.TextInput(attrs={'class': 'form-control'}),
        }