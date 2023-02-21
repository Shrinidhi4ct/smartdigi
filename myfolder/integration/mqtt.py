import paho.mqtt.client as paho
import json
import django

django.setup()
from django.conf import settings
from .models import *
from utils.constants import Constants

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # Get all the MQTT topics from the database
    mqtt_topics = MQTTSetup.objects.all()
    for topic in mqtt_topics:
        client.subscribe(topic.topic, qos=1)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # validate topic
    if msg.topic == Constants.IAQ_TOPIC:
        # convert payload to json
        try:
            payload = json.loads(msg.payload)
            room_id = payload["deviceId"]
            # save data to database
            aqi = AQI.objects.create(room=room_id, data=payload)
            aqi.save()
        except Exception as e:
            pass
    elif msg.topic == Constants.PEOPLE_COUNT_TOPIC:
        # convert payload to json
        try:
            payload = json.loads(msg.payload)
            room_id = payload["deviceId"]
            # save data to database
            footfall = FootFall.objects.create(room=room_id, data=payload)
            footfall.save()
        except Exception as e:
            pass


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")


# defining client
client = paho.Client(
    client_id="4CT_MANAGEMENT_SERVER",
    clean_session=True,
    userdata=None,
    protocol=paho.MQTTv311,
)


# adding callbacks to client
client.on_connect = on_connect
client.on_message = on_message


try:
    client.connect(
        host=settings.MQTT_SERVER,
        port=settings.MQTT_PORT,
        keepalive=60,
        bind_address="",
    )
except Exception as e:
    print("Connection failed: " + str(e))
