from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    View,
)
from utils.custom_mixin import CustomUserAccessRequiredMixin
from ..models import *
from ..forms import FloorSetupForm


class FloorListView(LoginRequiredMixin, CustomUserAccessRequiredMixin, ListView):
    """
    List all the Floors in the database
    """

    # HTML Template
    template_name = "restroom/floor_list.html"
    # Model to use
    model = FloorSetup
    # Context object name in the template
    context_object_name = "floors"


class FloorCreateView(LoginRequiredMixin, CustomUserAccessRequiredMixin, CreateView):
    """
    Create new floor from admin dashboard
    """

    # Model
    model = FloorSetup
    # Template Name
    template_name = "restroom/create_floor.html"
    # Forms
    form_class = FloorSetupForm
    # Success
    success_message = "Floor Created Successfully!"
    success_url = reverse_lazy("floor_list")

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, str(form.errors))
        return super().form_invalid(form)


class FloorUpdateView(LoginRequiredMixin, CustomUserAccessRequiredMixin, UpdateView):
    """
    Update existing floor from admin dashboard
    """

    # Model
    model = FloorSetup
    # Template Name
    template_name = "restroom/update_floor.html"
    # Forms
    form_class = FloorSetupForm
    # Success
    success_message = "Floor Updated Successfully!"
    success_url = reverse_lazy("floor_list")

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, str(form.errors))
        return super().form_invalid(form)


class FloorDeleteView(LoginRequiredMixin, CustomUserAccessRequiredMixin, View):
    """
    Delete existing floor from admin dashboard
    """

    # Model
    model = FloorSetup
    # Success
    success_message = "Floor Deleted Successfully!"
    success_url = reverse_lazy("floor_list")

    def get(self, request, pk):
        # get reasons
        floor = self.model.objects.get(pk=pk)
        # Delete retrived reasons
        floor.delete()
        # Success message
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return redirect(self.success_url)
