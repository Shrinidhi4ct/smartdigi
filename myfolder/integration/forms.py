from django import forms
from .models import *


class MQTTSetupForm(forms.ModelForm):
    """
    Form for creating a new MqttSetup
    """

    class Meta:
        model = MQTTSetup
        fields = ["name", "topic", "is_active"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Name"}
            ),
            "topic": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Topic"}
            ),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
