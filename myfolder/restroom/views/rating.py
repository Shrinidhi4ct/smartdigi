from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View
from utils.custom_mixin import CustomUserAccessRequiredMixin

from ..forms import RatingForm
from ..models import *


class RatingListView(LoginRequiredMixin, CustomUserAccessRequiredMixin, ListView):
    """
    List all the ratings in the database
    """

    # HTML Template
    template_name = "restroom/rating_list.html"
    # Model to use
    model = RatingSetup
    # Context object name in the template
    context_object_name = "ratings"


class RatingCreateView(LoginRequiredMixin, CustomUserAccessRequiredMixin, CreateView):
    """
    Create new room from admin dashboard
    """

    # Model
    model = RatingSetup
    # Template Name
    template_name = "restroom/create_rating.html"
    # Forms
    form_class = RatingForm
    # Success
    success_message = "Rating Metric Created successfully!"
    success_url = reverse_lazy("rating_list")

    def post(self, request, *args, **kwargs):
        # if db contain active data don't allow to create new data
        if RatingSetup.objects.filter(is_active=True).exists():
            messages.add_message(
                self.request, messages.WARNING, "Active Rating Metric already exist!"
            )
            return redirect("rating_list")
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, str(form.errors))
        return super().form_invalid(form)


class RatingUpdateView(LoginRequiredMixin, CustomUserAccessRequiredMixin, UpdateView):
    """
    Update existing ratings from admin dashboard
    """

    # Model
    model = RatingSetup
    # Template Name
    template_name = "restroom/update_rating.html"
    # Forms
    form_class = RatingForm
    # Success
    success_message = "Rating Updated Successfully!"
    success_url = reverse_lazy("rating_list")

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, str(form.errors))
        return super().form_invalid(form)


class RatingDeleteView(LoginRequiredMixin, CustomUserAccessRequiredMixin, View):
    """
    Delete existing rating from admin dashboard
    """

    # Model
    model = RatingSetup
    # Success
    success_message = "Rating Deleted Successfully!"
    success_url = reverse_lazy("rating_list")

    def get(self, request, pk):
        # get reasons
        rating = self.model.objects.get(pk=pk)
        # Delete retrived reasons
        rating.delete()
        # Success message
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return redirect(self.success_url)
