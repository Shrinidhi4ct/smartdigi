from django.db.models.signals import post_save
from django.dispatch import receiver

from utils.constants import Constants, Threshold
from restroom.models import Alert_history
from .models import AQI



@receiver(post_save, sender=AQI)
def post_save_aqi(sender, instance, created, **kwargs):
    """
        Check the values and send alert email
    """
    if created:
        aqi_data = instance.data

        # Validate the data
        # Temperature validation
        if aqi_data[Constants.TEMPERATURE] <= Threshold.TEMP_BELOW:
            alert_create(Constants.TEMPERATURE, aqi_data[Constants.TEMPERATURE], "below")
        elif aqi_data[Constants.TEMPERATURE] >= Threshold.TEMP_ABOVE:
            alert_create(Constants.TEMPERATURE, aqi_data[Constants.TEMPERATURE], "above")
        else:
            pass
        
        # Humidity validation
        if aqi_data[Constants.HUMIDITY] <= Threshold.HUM_BELOW:
            alert_create(Constants.HUMIDITY, aqi_data[Constants.HUMIDITY], "below")
        elif aqi_data[Constants.HUMIDITY] >= Threshold.HUM_ABOVE:
            alert_create(Constants.HUMIDITY, aqi_data[Constants.HUMIDITY], "above")
        else:
            pass
        
        # CO2 validation
        if aqi_data[Constants.CO2] <= Threshold.CO2_BELOW:
            alert_create(Constants.CO2, aqi_data[Constants.CO2], "below")
        elif aqi_data[Constants.CO2] >= Threshold.CO2_ABOVE:
            alert_create(Constants.CO2, aqi_data[Constants.CO2], "above")
        else:
            pass
        
        # Ammonia validation
        if aqi_data[Constants.AMMONIA] <= Threshold.AMMONIA_BELOW:
            alert_create(Constants.AMMONIA, aqi_data[Constants.AMMONIA], "below")
        elif aqi_data[Constants.AMMONIA] >= Threshold.AMMONIA_ABOVE:
            alert_create(Constants.AMMONIA, aqi_data[Constants.AMMONIA], "above")
        else:
            pass
        
        # TVOC validation
        if aqi_data[Constants.TVOC] <= Threshold.TVOC_BELOW:
            alert_create(Constants.TVOC, aqi_data[Constants.TVOC], "below")
        elif aqi_data[Constants.TVOC] >= Threshold.TVOC_ABOVE:
            alert_create(Constants.TVOC, aqi_data[Constants.TVOC], "above")
        else:
            pass


def alert_create(parameter, value, threshold):
    """
        Create alert history
    """
    try:
        alert = Alert_history.objects.create(
            parameter=parameter,
            data = {"value": value, "threshold": threshold},
        )
        alert.save()
    except Exception as e:
        print(e)