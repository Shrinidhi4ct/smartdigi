from datetime import datetime, timedelta
from django.views.generic import View
from django.http import JsonResponse
from integration.models import FootFall


class HeatMapDataView(View):

    def get(self, request, pk):

        current_month = datetime.now().month
        current_week = datetime.now().isocalendar()[1]

        # get room name from args
        room_identifier = pk

        data = FootFall.objects.filter(room=room_identifier,
                                        created_at__month=current_month,
                                        created_at__week=current_week).all()

        people_in = {
            0: [0] * 24,
            1: [0] * 24,
            2: [0] * 24,
            3: [0] * 24,
            4: [0] * 24,
            5: [0] * 24,
            6: [0] * 24,
        }

        # Iterating through the data and adding the number of people in to the people_in dictionary.
        for item in data:
            day = item.created_at.weekday()
            hour = item.created_at.hour
            if item.data and item.data.get("ENTRY"):
                people_in[day][hour] += item.data.get("ENTRY")
            
        
        return JsonResponse(people_in, status=200, safe=False)


class LineChartDataView(View):

    def get(self, request, pk):
        # get room name from args
        current_month = datetime.now().month
        room_identifier = pk

        data = FootFall.objects.filter(room=room_identifier, created_at__month=current_month).all()

        people_in = [0] * 31

        # Iterating through the data and adding the number of people in to the people_in dictionary.
        for item in data:
            day = item.created_at.day
            if item.data and item.data.get("ENTRY"):
                people_in[day] += item.data.get("ENTRY")

        return JsonResponse(people_in, status=200, safe=False)


class LineChartFullDataView(View):

    def get(self, request):

        current_month = datetime.now().month

        data = FootFall.objects.filter(created_at__month=current_month).all()


        people_in = {}
        for item in data:
            room = item.room
            day = item.created_at.day
            if room not in people_in:
                people_in[room] = [0] * 31
            if item.data and item.data.get("ENTRY"):
                people_in[room][day] += item.data.get("ENTRY")

        return JsonResponse(people_in, status=200, safe=False)
