from asgiref.sync import sync_to_async
import json
from .models import MQTTSetup, AQI
from restroom.models import RoomSetup


def get_mqtt_topics():
    topics = MQTTSetup.objects.filter(is_active=True).all()
    topic_list = []
    for row in topics:
        topic_list.append(row.topic)
    return topic_list


async def save_mqtt_data(message):
    """
    Save aqi data to database
    """
    try:
        topic = message["topic"]
        # convert payload to json
        payload = json.loads(message["payload"])
        room = payload["deviceId"]
        aqi = sync_to_async(AQI.objects.create(data=payload, room=room))
        aqi.save()
        print("Data saved successfully")
        return f"Data saved successfully"
    except Exception as e:
        print(e)
        return f"Error saving data: {str(e)}"
