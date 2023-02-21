from django import forms

from django.contrib.auth.forms import AuthenticationForm
from .models import *


class ReasonSetupForm(forms.ModelForm):
    """
    Form for creating a new reason
    """

    class Meta:
        model = RestroomReasonSetup
        fields = ["name", "display_text", "description", "display_image", "is_active"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Name"}
            ),
            "display_text": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Display Text"}
            ),
            "description": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Description"}
            ),
            "display_image": forms.FileInput(
                attrs={"class": "form-control", "placeholder": "Display Image"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class CheckListSetupForm(forms.ModelForm):
    """
    Form for creating a new CheckList
    """

    class Meta:
        model = CheckListSetup
        fields = ["name", "display_text", "description", "display_image", "is_active"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Checklist Name"}
            ),
            "display_text": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Display Text"}
            ),
            "description": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Description"}
            ),
            "display_image": forms.FileInput(
                attrs={"class": "form-control", "placeholder": "Display Image"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class RoomSetupForm(forms.ModelForm):
    """
    Form for create / Update New Room
    """

    reason = forms.ModelMultipleChoiceField(
        queryset=RestroomReasonSetup.objects.filter(is_active=True).all(),
        widget=forms.SelectMultiple(
            attrs={"class": "form-control", "multiple": "multiple"}
        ),
    )

    class Meta:
        model = RoomSetup
        fields = [
            "name",
            "description",
            "room_shape",
            "reason",
            "room_location",
            "is_active",
            "room_idenfier",
        ]
        # Floor Choices
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Room Name"}
            ),
            "description": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Description"}
            ),
            "room_shape": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Room Shape"}
            ),
            "room_location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Room Location"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "room_idenfier": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Room Identifier(sensor)",
                }
            ),
        }


class FloorSetupForm(forms.ModelForm):
    """
    Form for create / Update Floor
    """

    class Meta:
        model = FloorSetup
        fields = ["name", "description", "floor_map", "is_active"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Floor Name"}
            ),
            "description": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Description"}
            ),
            "floor_map": forms.FileInput(
                attrs={"class": "form-control", "placeholder": "Floor Map"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class CustomLoginForm(AuthenticationForm):
    """
    Custom login form
    """

    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
            }
        ),
    )


class RatingForm(forms.ModelForm):
    """
    Form for creating a new Rating metrics
    """

    class Meta:
        model = RatingSetup
        fields = ["name", "positive_image", "negative_image", "is_active"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Name"}
            ),
            "positive_image": forms.FileInput(
                attrs={"class": "form-control", "placeholder": "Positive Image"}
            ),
            "negative_image": forms.FileInput(
                attrs={"class": "form-control", "placeholder": "Negative Image"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
