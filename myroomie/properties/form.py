
from django import forms
from .models import Room


class RoomForm(forms.ModelForm):

    class Meta:
        model = Room

        fields = [
            'title',
            'description',
            'location',
            'latitude',
            'longitude',
            'rent',
            'room_type',
            'available_from',
            'amenities',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter room title'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your room',
                'rows': 4
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter room location'
            }),

            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter latitude'
            }),

            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter longitude'
            }),

            'rent': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Monthly rent'
            }),

            'room_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'available_from': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),

            'amenities': forms.CheckboxSelectMultiple(),
        }
