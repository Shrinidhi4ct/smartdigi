from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View
from utils.custom_mixin import CustomUserAccessRequiredMixin

from ..forms import RoomSetupForm
from ..models import *


class RoomListView(LoginRequiredMixin, CustomUserAccessRequiredMixin, ListView):
    """
    List all the rooms in the database
    """

    # HTML Template
    template_name = "restroom/room_list.html"
    # Model to use
    model = RoomSetup
    # Context object name in the template
    context_object_name = "rooms"


class RoomCreateView(LoginRequiredMixin, CustomUserAccessRequiredMixin, CreateView):
    """
    Create new room from admin dashboard
    """

    # Model
    model = RoomSetup
    # Template Name
    template_name = "restroom/create_room.html"
    # Forms
    form_class = RoomSetupForm
    # Floor
    floors = FloorSetup.objects.filter(is_active=True).all()
    # Success
    success_message = "Room Created Successfully!"
    success_url = reverse_lazy("room_list")

    def get(self, request, *args, **kwargs):

        return render(
            request,
            self.template_name,
            {"form": self.form_class, "floors": self.floors},
        )

    def post(self, request, *args, **kwargs):
        """
        create new room
        """
        values = request.POST

        # Format the data
        data = {
            "name": values.get("name"),
            "description": values.get("description"),
            "floor_id": values.get("floor_id"),
            "room_shape": values.get("im[0][shape]"),
            "room_location": values.get("room_location"),
            "room_idenfier": values.get("room_idenfier"),
            "reason": values.getlist("reason"),
            "is_active": True if values.get("is_active") == "on" else False,
        }

        try:
            self.model.objects.create(**data)
            messages.success(request, "Room added successfully")
            return redirect("room_list")
        except Exception as e:
            return render(
                request,
                self.template_name,
                {"form": self.form_class, "floors": self.floors, "error": e},
            )


class RoomUpdateView(LoginRequiredMixin, CustomUserAccessRequiredMixin, UpdateView):
    """
    Update existing room from admin dashboard
    """

    # Model
    model = RoomSetup
    # Template Name
    template_name = "restroom/update_room.html"
    # Forms
    form_class = RoomSetupForm
    # Floor
    floors = FloorSetup.objects.filter(is_active=True).all()
    # Success
    success_message = "Room Updated Successfully!"
    success_url = reverse_lazy("room_list")

    def get(self, request, *args, **kwargs):

        room = self.model.objects.get(id=kwargs.get("pk"))
        return render(
            request,
            self.template_name,
            {"form": self.form_class, "floors": self.floors, "room": room},
        )

    def post(self, request, *args, **kwargs):
        """
        Update room
        """
        values = request.POST
        room = self.model.objects.get(id=kwargs.get("pk"))

        # Format the data
        data = {
            "name": values.get("name"),
            "description": values.get("description"),
            "floor_id": values.get("floor_id"),
            "room_shape": values.get("im[0][shape]"),
            "room_location": values.get("room_location"),
            "room_idenfier": values.get("room_idenfier"),
            "reason": values.getlist("reason"),
            "is_active": True if values.get("is_active") == "on" else False,
        }
        try:
            room.name = data.get("name")
            room.description = data.get("description")
            room.floor_id = data.get("floor_id")
            room.room_shape = data.get("room_shape")
            room.room_location = data.get("room_location")
            room.room_idenfier = data.get("room_idenfier")
            room.reason = data.get("reason")
            room.is_active = data.get("is_active")
            room.save()
            messages.success(request, "Room updated successfully")
            return redirect("room_list")
        except Exception as e:
            return render(
                request,
                self.template_name,
                {
                    "form": self.form_class,
                    "floors": self.floors,
                    "room": room,
                    "error": e,
                },
            )

    def form_valid(self, form):
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.WARNING, str(form.errors))
        return super().form_invalid(form)


class RoomDeleteView(LoginRequiredMixin, CustomUserAccessRequiredMixin, View):
    """
    Delete existing room from admin dashboard
    """

    # Model
    model = RoomSetup
    # Success
    success_message = "Room Deleted Successfully!"
    success_url = reverse_lazy("room_list")

    def get(self, request, pk):
        # get reasons
        room = self.model.objects.get(pk=pk)
        # Delete retrived reasons
        room.delete()
        # Success message
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return redirect(self.success_url)
