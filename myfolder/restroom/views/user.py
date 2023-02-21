from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from utils.custom_mixin import CustomUserAccessRequiredMixin


class UserListView(LoginRequiredMixin, CustomUserAccessRequiredMixin, ListView):
    """
    List all the user in the database
    """

    # HTML Template
    template_name = "registration/user_list.html"
    # Model to use
    model = User
    # Context object name in the template
    context_object_name = "users"


class UserCreateView(LoginRequiredMixin, CustomUserAccessRequiredMixin, CreateView):
    """
    Create a new user
    """

    # HTML Template
    template_name = "registration/user_create.html"
    # Model to use
    model = User
    # Success URL
    success_url = reverse_lazy("user_list")

    def get(self, request, *args, **kwargs):
        """
        Get the request and render the form
        """
        # Render the form
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        """
        Save new user in the database
        """
        # Get the form data
        data = request.POST

        # Password validation
        if data["password"] != data["password2"]:
            messages.error(request, "Passwords do not match")
            return redirect("user_create")

        # check if user exists
        if self.model.objects.filter(username=data["username"]).exists():
            messages.error(request, "User already exists")
            return redirect("user_create")

        # Role
        is_staff = True if data["role"] == "admin" else False
        is_superuser = True if data["role"] == "admin" else False
        # active status
        is_active = True if data["is_active"] == "on" else False
        # Create the user
        try:
            self.model.objects.create_user(  # type: ignore
                username=data["username"],
                password=data["password"],
                email=data["email"],
                is_staff=is_staff,
                is_active=is_active,
                is_superuser=is_superuser,
            )
            messages.success(request, "User created successfully")
            return redirect("user_list")
        except Exception as e:
            messages.error(request, "Error creating user")
            return redirect("user_create")


class UserDeleteView(LoginRequiredMixin, CustomUserAccessRequiredMixin, DeleteView):
    """
    Delete a user
    """

    # Model
    model = User
    # Success
    success_message = "User Deleted Successfully!"
    success_url = reverse_lazy("user_list")

    def get(self, request, pk):
        # get user
        user = self.model.objects.get(pk=pk)
        # Delete retrived reasons
        user.delete()
        # Success message
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return redirect(self.success_url)
