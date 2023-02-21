from datetime import datetime
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    View,
)

from utils.custom_mixin import CustomUserAccessRequiredMixin

from ..models import *
from ..forms import ReasonSetupForm
from ..scripts import get_ticket_count_info


class ReasonListView(LoginRequiredMixin, CustomUserAccessRequiredMixin, ListView):
    """
    List all the reasons in the database
    """

    # HTML Template
    template_name = "restroom/reason_list.html"
    # Model to use
    model = RestroomReasonSetup
    # Context object name in the template
    context_object_name = "reasons"


class ReasonCreateView(LoginRequiredMixin, CustomUserAccessRequiredMixin, CreateView):
    """
    Create new reason from admin dashboard
    """

    # Model
    model = RestroomReasonSetup
    # Template Name
    template_name = "restroom/create_reason.html"
    # Fields
    fields = ["name", "display_text", "description", "display_image", "is_active"]
    # Success
    success_message = "Reason Created Successfully!"
    success_url = reverse_lazy("reason_list")

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, str(form.errors))
        return super().form_invalid(form)


class ReasonUpdateView(LoginRequiredMixin, CustomUserAccessRequiredMixin, UpdateView):
    """
    Update existing reasin from admin dashboard
    """

    # Model
    model = RestroomReasonSetup
    # Template Name
    template_name = "restroom/update_reason.html"
    # Forms
    form_class = ReasonSetupForm
    # Success
    success_message = "Reason Updated Successfully!"
    success_url = reverse_lazy("reason_list")

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, str(form.errors))
        return super().form_invalid(form)


class ReasonDeleteView(LoginRequiredMixin, CustomUserAccessRequiredMixin, View):
    """
    Delete existing reason from admin dashboard
    """

    # Model
    model = RestroomReasonSetup
    # Success
    success_message = "Reason Deleted Successfully!"
    success_url = reverse_lazy("reason_list")

    def get(self, request, pk):
        # get reasons
        reason = self.model.objects.get(pk=pk)
        # Delete retrived reasons
        reason.delete()
        # Success message
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return redirect(self.success_url)
