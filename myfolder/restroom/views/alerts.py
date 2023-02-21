from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages as message
from ..models import AlertConditions


class AlertConditionsView(View):
    """
        Manage Email alerts 
    """

    model = AlertConditions
    template_name = "restroom/alerts.html"

    def get(self, request, *args, **kwargs):

        context = {
            "alerts": AlertConditions.objects.first(),
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        data = request.POST

        print(data)

        if data is not None:
            alert = AlertConditions.objects.first()
            if alert:
                alert.email = data.get("email")
                alert.save()
            else:
                AlertConditions.objects.create(
                    email=data.get("email"),
                    name=data.get("name"),
                    is_active=True
                )
        
        message.add_message(request, message.SUCCESS, "Email alerts updated successfully")
        return redirect("alerts")