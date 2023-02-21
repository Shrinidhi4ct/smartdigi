from .models import RoomSetup


def room_list(request):
    """
    List all the rooms order by created_at
    """
    room_list = RoomSetup.objects.filter(is_active=True).all().order_by("name")
    return {"room_list": room_list}
