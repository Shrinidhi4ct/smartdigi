from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, View
from django.contrib import messages

from utils.custom_mixin import CustomUserAccessRequiredMixin

from ..models import *


# Create your views here.
class MaintenaceDashboardView(LoginRequiredMixin, TemplateView):

    template_name = "maintenance/dashboard.html"

    model = Tickets
    room_model = RoomSetup
    success_message = "Checklist has been updated successfully"

    def get(self, request):
        """
        :param request: The request is an HttpRequest object. It contains metadata about the request,
        such as the HTTP method
        :return: The get method is returning the context dictionary.
        """
        # Get all unresolved tickets
        unresolved_tickets = self.model.objects.filter(
            is_resolved=False, feedback=False
        ).all()
        # Get checklist
        check_list = CheckListSetup.objects.filter(is_active=True).all()
        # Room List
        room_list = RoomSetup.objects.filter(is_active=True).all()

        context = {
            "tickets": unresolved_tickets,
            "check_list": check_list,
            "room_list": room_list,
        }

        return render(request, self.template_name, context)

    def post(self, request):
        """
        :param request: The request is an HttpRequest object. It contains metadata about the request,
        such as the HTTP method
        :return: The post method is returning the context dictionary.
        """
        try:
            # Get data
            data = request.POST
            # URL Parameter (Room id / Name)
            room_id = self.room_model.objects.get(id=data["room"])

            data = {}
            for key, values in request.POST.lists():
                if key != "csrfmiddlewaretoken" and key != "room":
                    key = key.lower().replace(" ", "_")
                    data[key] = True if values[0] == "on" else False

            check_list = CheckList.objects.create(
                checklist=data, room=room_id, created_by=request.user
            )
            check_list.save()
            messages.add_message(self.request, messages.SUCCESS, self.success_message)
            return redirect("maintenance_dashboard")
        except Exception as e:
            messages.add_message(self.request, messages.ERROR, "Something went wrong")
            return redirect("maintenance_dashboard")


class MaintenanceTicketUpdateView(LoginRequiredMixin, View):
    """
    Updating resolved status of the maintenance Ticket
    """

    model = Tickets
    success_message = "Ticket has been resolved successfully"

    def get(self, request, pk):
        """
        :param request: The request is an HttpRequest object. It contains metadata about the request,
        such as the HTTP method
        :param pk: The primary key of the ticket
        :return: The get method is returning the context dictionary.
        """
        try:
            ticket = Tickets.objects.get(pk=pk)
            ticket.updated_by = request.user
            ticket.is_resolved = True
            ticket.save()
            messages.add_message(self.request, messages.SUCCESS, self.success_message)
            return redirect("maintenance_dashboard")
        except Exception as e:
            messages.add_message(self.request, messages.ERROR, "Something went wrong")
            return redirect("maintenance_dashboard")


class MaintenanceTicketByRoomView(LoginRequiredMixin, View):
    """
        Retrive all unresolved tickets by room and return response as json
    """
    
    model = Tickets

    def get(self, request, pk):
        """
        :param request: The request is an HttpRequest object. It contains metadata about the request,
        such as the HTTP method
        :param pk: The primary key of the room
        :return: The get method is returning the context dictionary.
        """
        try:
            tickets = self.model.objects.filter(
                room=pk, is_resolved=False, feedback=False
            ).all()
            return JsonResponse(
                {
                    "tickets": [
                        {
                            "id": ticket.id,
                            "room": ticket.room.name,
                            "reason": ticket.reason
                        }
                        for ticket in tickets
                    ]
                }
            )
        except Exception as e:
            return JsonResponse({"error": "Something went wrong"}, status=500)
    