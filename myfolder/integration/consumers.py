from mqttasgi.consumers import MqttConsumer
from .scripts import get_mqtt_topics, save_mqtt_data

topics = get_mqtt_topics()


class MyMqttConsumer(MqttConsumer):
    async def connect(self):
        for topic in topics:
            await self.subscribe(topic, 2)
        # await self.subscribe('topic', 2)

    async def disconnect(self, code):
        for topic in topics:
            await self.unsubscribe(topic)

    async def receive(self, mqtt_message):
        await save_mqtt_data(mqtt_message)
