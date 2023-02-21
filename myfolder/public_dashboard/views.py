import ast
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from django.http import JsonResponse
from django.contrib import messages

from restroom.models import RestroomReasonSetup, Tickets, RoomSetup, RatingSetup
from integration.models import AQI
from utils.constants import Threshold

# Create your views here.
class HomePageView(TemplateView):

    model = RestroomReasonSetup
    ticket_model = Tickets
    room_model = RoomSetup
    rating_model = RatingSetup
    template_name = "dashboard/template_1.html"
    not_done_template = "errors/404.html"
    success_message = "Thank you for your feedback"
    failer_message = "Something went wrong"

    def get(self, request, pk):
        """
        It gets the data from the database and passes it to the template

        :param request: The request is an HttpRequest object
        :return: The render function is being returned.
        """
        try:
            # Get Room information
            room = self.room_model.objects.get(id=pk)
            # GET IAQ Information
            iaq = self.get_latest_iaq_data_by_room(pk)
            # Threshold
            threshold = Threshold.__dict__
            # Get all reasons for the room
            context = {
                "reasons": self.format_and_get_reasons(room.reason),
                "iaq_data": iaq,
                "threshold": threshold,
                "room": room,
                "ratings": self.rating_model.objects.filter(is_active=True).first(),
            }
            return render(request, self.template_name, context)
        except Exception as e:
            print(e)
            # If room is not found redirect to 404
            return render(request, self.not_done_template, {"error": e})

    def post(self, request, pk):
        """
        Save form data
        """
        # URL Parameter (Room id / Name)
        room_id = self.room_model.objects.get(id=pk)
        try:
            # Get data
            data = request.POST
            reason = ""
            if len(data) != 1:
                for key, values in data.lists():
                    if key != "csrfmiddlewaretoken":
                        # get actual reason from reason table
                        d = self.model.objects.get(id=key)
                        # Get reason
                        reason += d.name + ":"
                ticket = self.ticket_model(reason=reason, room=room_id)
                ticket.save()

                messages.success(request, self.success_message)
                return redirect("home", pk=room_id.id)
            else:
                messages.error(request, "Select atleast one reason")
                return redirect("home", pk=room_id.id)
        except Exception as e:
            messages.error(request, self.failer_message)
            return redirect("home", pk=room_id.id)

    def format_and_get_reasons(self, reason):
        """
        Format the reason
        """
        # escape_char = ["[", "]", "'", " ", ",", ">", "<"]
        # reason_ids = []
        # convert reason string to list
        integer_list = ast.literal_eval(reason)
        # Use map() to convert the elements of the list to integers
        reason_ids = list(map(int, integer_list))

        reason_list = self.model.objects.filter(id__in=reason_ids, is_active=True).all()

        return reason_list

    def get_latest_iaq_data_by_room(self, pk):
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


class PositiveFeebackView(View):
    """
    Positive Feedback View
    """

    model = Tickets
    room_model = RoomSetup

    def get(self, request, pk):
        """
        It gets the data from the database and passes it to the template

        :param request: The request is an HttpRequest object
        :return: The render function is being returned.
        """
        try:
            # Room id
            room_instance = self.room_model.objects.get(id=pk)
            if room_instance:
                # add new ticket
                ticket = self.model(room=room_instance, reason={}, feedback=True)
                ticket.save()
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error"})
        except Exception as e:
            return JsonResponse({"status": "error", "error": e})