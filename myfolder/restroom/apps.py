from django.apps import AppConfig


class RestroomConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "restroom"

    def ready(self):
        import restroom.signals

        # from integration.models import FootFall
        # from datetime import datetime, timedelta
        # import random
        # # dummy data addd
        # room_ids = ["WashRoom1", "WashRoom2"]
        # # choose random room
        # room_id = random.choice(room_ids)
        # # save data to database
        # payload = {"ENTRY": random.randint(0, 5),
        #             "Time": None, 
        #             "deviceId": "WashRoom1"
        #             }


        # for i in range(1, 50):
        #     # every loop created_at value should increase by 1hr
        #     created_at = datetime.now() + timedelta(hours=i)
        #     print(created_at)
        #     footfall = FootFall.objects.create(room=room_id, data=payload, created_at=created_at)
        #     footfall.save()
