from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    View,
)

from utils.custom_mixin import CustomUserAccessRequiredMixin
from ..models import *
from ..forms import CheckListSetupForm


class CheckListView(LoginRequiredMixin, CustomUserAccessRequiredMixin, ListView):
    """
    List all the Checklist in the database
    """

    # HTML Template
    template_name = "restroom/check_list.html"
    # Model to use
    model = CheckListSetup
    # Context object name in the template
    context_object_name = "checklist"


class CheckListCreateView(
    LoginRequiredMixin, CustomUserAccessRequiredMixin, CreateView
):
    """
    Create new Checklist from admin dashboard
    """

    # Model
    model = CheckListSetup
    # Template Name
    template_name = "restroom/create_checklist.html"
    # Fields
    fields = ["name", "display_text", "description", "display_image", "is_active"]
    # Success
    success_message = "Reason Created Successfully!"
    success_url = reverse_lazy("check_list")

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, str(form.errors))
        return super().form_invalid(form)


class CheckListUpdateView(
    LoginRequiredMixin, CustomUserAccessRequiredMixin, UpdateView
):
    """
    Update existing reasin from admin dashboard
    """

    # Model
    model = CheckListSetup
    # Template Name
    template_name = "restroom/update_checklist.html"
    # Forms
    form_class = CheckListSetupForm
    # Success
    success_message = "Checklist Updated Successfully!"
    success_url = reverse_lazy("check_list")

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, str(form.errors))
        return super().form_invalid(form)


class CheckListDeleteView(LoginRequiredMixin, CustomUserAccessRequiredMixin, View):
    """
    Delete existing Checklist from admin dashboard
    """

    # Model
    model = CheckListSetup
    # Success
    success_message = "Checklist Deleted Successfully!"
    success_url = reverse_lazy("check_list")

    def get(self, request, pk):
        # get Checklist
        check_list = self.model.objects.get(pk=pk)
        # Delete retrived Checklist
        check_list.delete()
        # Success message
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return redirect(self.success_url)
