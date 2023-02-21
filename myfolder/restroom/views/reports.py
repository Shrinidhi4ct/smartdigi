import csv
from datetime import datetime
from django.shortcuts import HttpResponse, render
from django.views.generic import View
from django.contrib import messages
from integration.models import AQI

from ..models import Tickets, RoomSetup
from utils.constants import Constants


class ReportGeneralView(View):
    """
    Report main page view
    """

    template_name = "restroom/reports.html"
    ticket_model = Tickets
    aqi_model = AQI
    current_month = datetime.now().month
    current_year = datetime.now().year
    currnet_week = datetime.now().isocalendar()[1]

    def get(self, request):
        """
        :param request: The request is an HttpRequest object. It contains metadata about the request,
        such as the HTTP method
        :return: The get method is returning the context dictionary.
        """
        return render(request, self.template_name)

    def post(self, request):
        """
        :param request: The request is an HttpRequest object. It contains metadata about the request,
        """
        try:
            # Read form data
            form = request.POST
            # Get the data from the form
            report_type = form.get("type")
            room_type = form.get("room_type")
            report_range = form.get("range")

            if report_type == Constants.REPORT_TICKET:
                # Get the tickets data
                tickets_data = self.get_tickets_data(report_range, room_type)
                # file name
                file_name = f"{report_type}_{report_range}.csv"
                # response
                response = HttpResponse(content_type="text/csv")
                response["Content-Disposition"] = f'attachment; filename="{file_name}"'
                # write the data to the response
                writer = csv.writer(response)
                writer.writerow(
                    [
                        "id",
                        "room",
                        "reason",
                        "feedback",
                        "is_resolved",
                        "created_at",
                        "modified_at",
                        "updated_by",
                    ]
                )
                for ticket in tickets_data:
                    writer.writerow(
                        [
                            ticket.id,
                            ticket.room,
                            ticket.reason,
                            ticket.feedback,
                            ticket.is_resolved,
                            ticket.created_at,
                            ticket.modified_at,
                            ticket.updated_by,
                        ]
                    )
                # messages.add_message(
                #     self.request, messages.SUCCESS, "Report generated successfully"
                # )

                return response
            elif report_type == Constants.REPORT_AQI:
                messages.add_message(
                    self.request, messages.ERROR, "Table is not integrated yet"
                )
                return render(request, self.template_name)
            elif report_type == Constants.REPORT_FOOTFALL:
                messages.add_message(
                    self.request, messages.ERROR, "Table is not integrated yet"
                )
                return render(request, self.template_name)

        except Exception as e:
            messages.error(request, "Something went wrong. Please try again later.")
            return render(request, self.template_name)

    def get_tickets_data(self, report_range, room_type):
        """
        :param report_range: The report range is the range of the report
        """
        try:
            # get all the tickets
            tickets = self.ticket_model.objects.all()

            # Get the tickets data
            if report_range == Constants.REPORT_RANGE_DAY:
                # Filte only the tickets created today
                tickets = tickets.filter(created_at__date=datetime.now().date())
            elif report_range == Constants.REPORT_RANGE_WEEK:
                # Filte only the tickets created this week
                tickets = tickets.filter(created_at__week=self.currnet_week)
            elif report_range == Constants.REPORT_RANGE_MONTH:
                # Filte only the tickets created this month
                tickets = tickets.filter(created_at__month=self.current_month)
            elif report_range == Constants.REPORT_RANGE_YEAR:
                # Filte only the tickets created this year
                tickets = tickets.filter(created_at__year=self.current_year)
            elif report_range == Constants.REPORT_RANGE_ALL:
                # Get all the tickets
                tickets = tickets.all()

            # Filter the tickets by room type
            if room_type == Constants.REPORT_ROOM_TYPE_ALL:
                # Get all the tickets
                tickets = tickets.all()
            else:
                # Filter the tickets by room type
                tickets = tickets.filter(room_id=room_type)
            return tickets

        except Exception as e:
            raise e
