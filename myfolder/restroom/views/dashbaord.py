from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    TemplateView,
)

from utils.custom_mixin import CustomUserAccessRequiredMixin
from integration.models import AQI, FootFall

from ..models import *
from ..scripts import get_ticket_count_info
from utils.constants import Threshold

# Create your views here.
class TicketDashboardView(LoginRequiredMixin, CustomUserAccessRequiredMixin, TemplateView):

    template_name = "restroom/dashboards/ticket_dashboard.html"
    """ 
        ticket_count: The total number of tickets in the database
        ticket_count_day: The number of tickets created in the last 24 hours
        ticket_count_week: The number of tickets created in the last 7 days
        ticket_count_month: The number of tickets created in the last 30 days
        ticket_resolved_count_month: The number of tickets resolved in the last 30 days
        
        The function uses the datetime module to get the current date and time. It then uses the
        timedelta function to get the date and time for the last 24 hours, 7 days, and 30 days
        
        :param request: The request is an HttpRequest object. It contains metadata about the request,
        such as the HTTP method
    """
    model = Tickets

    def get(self, request):
        """
        :param request: The request is an HttpRequest object. It contains metadata about the request,
        such as the HTTP method
        :return: The get method is returning the context dictionary.
        """
        # Get all unresolved tickets
        unresolved_tickets = Tickets.objects.filter(
            is_resolved=False, feedback=False
        ).all()

        ticket_count = get_ticket_count_info()
        # Get the room list
        room_list = RoomSetup.objects.filter(is_active=True).all()
        # Checklist

        context = {
            "tickets": unresolved_tickets,
            "ticket_count": ticket_count["ticket_count"],
            "ticket_count_day": ticket_count["ticket_count_day"],
            "ticket_count_week": ticket_count["ticket_count_week"],
            "ticket_count_month": ticket_count["ticket_count_month"],
            "ticket_resolved_count_month": ticket_count["ticket_resolved_count_month"],
            "positive_count": ticket_count["positive_count"],
            "check_list": self.get_check_list_data(),
            "room_list": room_list,
        }
        return render(request, self.template_name, context)

    def get_check_list_data(self):
        """
        Get the checklist data from the database
        """
        check_list_data = CheckList.objects.filter(
            created_at__date=datetime.now().date()
        )
        data = []
        for row in check_list_data:
            data.append(
                {
                    "checklist": list(row.checklist.keys()),
                    "created_at": row.created_at,
                    "created_by": row.created_by,
                    "room": row.room.name if row.room else None,
                }
            )
        return data


class IAQDashboardView(LoginRequiredMixin, CustomUserAccessRequiredMixin, TemplateView):

    template_name = "restroom/dashboards/iaq_dashboard.html"
    model = AQI

    def get(self, request):
        """
        :param request: The request is an HttpRequest object. It contains metadata about the request,
        such as the HTTP method
        :return: The get method is returning the context dictionary.
        """
        iaq_data = self.get_latest_data_by_room()
        ff_data = self.get_latest_ff_data_by_room()
        # get all the variable inside the threshold class and convert it to dictionary
        threshold = Threshold.__dict__
        context = {
            "iaq_data": iaq_data,
            "ff_data": ff_data,
            "threshold": threshold,
        }
        return render(request, self.template_name, context)

    def get_latest_data_by_room(self):
        """
        Get the latest data by room
        """
        room_list = RoomSetup.objects.filter(is_active=True).all().order_by("name")
        data = []
        for room in room_list:
           # Only specific room latest data 
            try:
                room_aqi_data = AQI.objects.filter(room=room.room_idenfier).latest("created_at")
            except AQI.DoesNotExist:
                room_aqi_data = None
            # if query does not exists
            data.append({
                "room": room.name,
                "aqi": room_aqi_data.data if room_aqi_data else None,
                "created_at": room_aqi_data.created_at if room_aqi_data else None,
            })
        return data

    def get_latest_ff_data_by_room(self):
        """
        Get the latest data by room
        """
        room_list = RoomSetup.objects.filter(is_active=True).all().order_by("name")
        data = []
        for room in room_list:
            in_data, out_data = 0, 0
            room_ff_data = FootFall.objects.filter(room=room.room_idenfier, created_at__date=datetime.now().date()).all()

            for row in room_ff_data:
                if row.data and row.data.get("ENTRY"):
                    in_data += row.data.get("ENTRY")
                if row.data and row.data.get("EXIT"):
                    out_data += row.data.get("EXIT")

            data.append({
                "room": room.name,
                "in": in_data,
                "out": out_data
            })
        return data

# Create your views here.
class RoomDashboardView(
    LoginRequiredMixin, CustomUserAccessRequiredMixin, TemplateView
):

    template_name = "restroom/dashboards/room_ticket_dashboard.html"
    """ 
        ticket_count: The total number of tickets in the database
        ticket_count_day: The number of tickets created in the last 24 hours
        ticket_count_week: The number of tickets created in the last 7 days
        ticket_count_month: The number of tickets created in the last 30 days
        ticket_resolved_count_month: The number of tickets resolved in the last 30 days
        
        The function uses the datetime module to get the current date and time. It then uses the
        timedelta function to get the date and time for the last 24 hours, 7 days, and 30 days
        
        :param request: The request is an HttpRequest object. It contains metadata about the request,
        such as the HTTP method
    """
    model = Tickets

    def get(self, request, pk):
        """
        :param request: The request is an HttpRequest object. It contains metadata about the request,
        such as the HTTP method
        :return: The get method is returning the context dictionary.
        """
        # Get all unresolved tickets
        unresolved_tickets = Tickets.objects.filter(
            is_resolved=False, feedback=False, room_id=pk
        ).all()

        ticket_count = get_ticket_count_info(pk)
        # Get the room list
        room_list = RoomSetup.objects.filter(is_active=True).all()
        # Checklist

        context = {
            "tickets": unresolved_tickets,
            "ticket_count": ticket_count["ticket_count"],
            "ticket_count_day": ticket_count["ticket_count_day"],
            "ticket_count_week": ticket_count["ticket_count_week"],
            "ticket_count_month": ticket_count["ticket_count_month"],
            "ticket_resolved_count_month": ticket_count["ticket_resolved_count_month"],
            "positive_count": ticket_count["positive_count"],
            "check_list": self.get_check_list_data(pk),
            "room_list": room_list,
            "room_name": RoomSetup.objects.get(id=pk).name,
        }
        return render(request, self.template_name, context)

    def get_check_list_data(self, room_id):
        """
        Get the checklist data from the database
        """
        check_list_data = CheckList.objects.filter(
            created_at__date=datetime.now().date(), room_id=room_id
        )
        data = []
        for row in check_list_data:
            data.append(
                {
                    "checklist": list(row.checklist.keys()),
                    "created_at": row.created_at,
                    "created_by": row.created_by,
                    "room": row.room.name if row.room else None,
                }
            )
        return data


class RoomIAQDashboardView(LoginRequiredMixin, CustomUserAccessRequiredMixin, TemplateView):

    template_name = "restroom/dashboards/room_iaq_dashboard.html"
    model = AQI

    def get(self, request, pk):
        """
        :param request: The request is an HttpRequest object. It contains metadata about the request,
        such as the HTTP method
        :return: The get method is returning the context dictionary.
        """
        try:
            iaq_data = self.get_latest_data_by_room(pk)
            ff_data = self.get_latest_ff_data_by_room(pk)
            context = {
                "iaq_data": iaq_data,
                "room_name": RoomSetup.objects.get(id=pk).name,
                "room_identifier": RoomSetup.objects.get(id=pk).room_idenfier,
                "ff_data": ff_data,
            }
            return render(request, self.template_name, context)
        except Exception as e:
            return redirect("dashboard")

    def get_latest_data_by_room(self, pk):
        """
        Get the latest data by room
        """
        room = RoomSetup.objects.filter(id=pk).first()
        data = []
        # Only specific room latest data
        try:
            room_aqi_data = AQI.objects.filter(room=room.room_idenfier).latest("created_at")
        except AQI.DoesNotExist:
            room_aqi_data = None
        # if query does not exists
        data.append({
            "room": room.name,
            "aqi": room_aqi_data.data if room_aqi_data else None,
            "created_at": room_aqi_data.created_at if room_aqi_data else None,
        })
        return data

    def get_latest_ff_data_by_room(self, pk):
        """
            Get Footfall data by room
        """
        try:
            in_data, out_data = 0, 0
            room = RoomSetup.objects.filter(id=pk).first()
            # retrive only today data
            footfall_data = FootFall.objects.filter(room=room.room_idenfier, 
                created_at__date=datetime.now().date()).all()
            for row in footfall_data:
                if row.data and row.data.get("ENTRY"):
                    in_data += row.data.get("ENTRY")
                if row.data and row.data.get("EXIT"):
                    out_data += row.data.get("EXIT")
            
            return {
                "in": in_data,
                "out": out_data,
            }
        except FootFall.DoesNotExist:
            in_data, out_data = 0, 0
            return {
                "in": in_data,
                "out": out_data,
            }
