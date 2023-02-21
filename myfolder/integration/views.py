from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View

from utils.custom_mixin import CustomUserAccessRequiredMixin

from .forms import MQTTSetupForm
from .models import MQTTSetup


# Create your views here.
class MQTTList(LoginRequiredMixin, CustomUserAccessRequiredMixin, ListView):
    """
    List all the rooms in the database
    """

    # HTML Template
    template_name = "integrations/mqtt/mqtt_topic_list.html"
    # Model to use
    model = MQTTSetup
    # Context object name in the template
    context_object_name = "topic"


class MQTTCreateView(LoginRequiredMixin, CustomUserAccessRequiredMixin, CreateView):
    """
    Create new room from admin dashboard
    """

    # Model
    model = MQTTSetup
    # Template Name
    template_name = "integrations/mqtt/create_mqtt_topic.html"
    # Forms
    form_class = MQTTSetupForm
    # Success
    success_message = "MQTT Topic Created Successfully!"
    success_url = reverse_lazy("mqtt_list")

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, str(form.errors))
        return super().form_invalid(form)


class MQTTUpdateView(LoginRequiredMixin, CustomUserAccessRequiredMixin, UpdateView):
    """
    Update existing rooms from admin dashboard
    """

    # Model
    model = MQTTSetup
    # Template Name
    template_name = "integrations/mqtt/update_mqtt_topic.html"
    # Forms
    form_class = MQTTSetupForm
    # Success
    success_message = "MQTT Topic Updated Successfully!"
    success_url = reverse_lazy("mqtt_list")

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, str(form.errors))
        return super().form_invalid(form)


class MQTTDeleteView(LoginRequiredMixin, CustomUserAccessRequiredMixin, View):
    """
    Delete existing rooms from admin dashboard
    """

    # model
    model = MQTTSetup
    # success
    success_message = "MQTT Topic Deleted Successfully!"
    success_url = reverse_lazy("mqtt_list")

    def get(self, request, *args, **kwargs):
        # Get the room
        topic = MQTTSetup.objects.get(id=self.kwargs["pk"])
        # Delete the room
        topic.delete()
        # Redirect to the list
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return redirect(self.success_url)
