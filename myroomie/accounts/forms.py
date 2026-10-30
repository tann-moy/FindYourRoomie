
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, UserProfile, Preference


# Bootstrap styling for all form fields
class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

            if isinstance(field.widget, forms.Select):
                field.widget.attrs["class"] = "form-select"

            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"


# Registration Form
class RegisterForm(BootstrapFormMixin, UserCreationForm):
    email = forms.EmailField()
    name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "role",
            "name",
            "password1",
            "password2",
        ]


# Profile Form
class ProfileForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "name",
            "profile_picture",
            "university",
            "department",
            "phone",
            "bio",
            "ref_loc",
            "ref_latitude",
            "ref_longitude",
        ]


# Preferences Form
class PreferenceForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Preference
        fields = [
            "location_preference",
            "budget_min",
            "budget_max",
            "gender_preference",
            "lifestyle",
            "preferred_room_type",
            "additional_notes",
            "food_type",
            "smoking",
            "sleep_time",
            "cleanliness",
        ]
