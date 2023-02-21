from django.db import models


class MQTTSetup(models.Model):
    """
    MQTT intergration setup model
    """

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    # ip_address = models.GenericIPAddressField(protocol="IPv4")
    # port = models.IntegerField()
    # username = models.CharField(max_length=100)
    # password = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "mqtt_setup"
        verbose_name = "MQTT Setup"
        verbose_name_plural = "MQTT Setup"

    def __str__(self):
        return self.name


# Create your models here.
class AQI(models.Model):
    """
    Air Quality sensor integration model
    """

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, default="AQI")
    data = models.JSONField()
    room = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "aqi"

    def __str__(self):
        return self.name


class FootFall(models.Model):
    """
    Footfall sensor integration model
    """

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, default="Footfall")
    data = models.JSONField()
    room = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "footfall"

    def __str__(self):
        return self.name