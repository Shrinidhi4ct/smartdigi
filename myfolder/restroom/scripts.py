from datetime import datetime
from .models import Tickets


def get_ticket_count_info(room_id="all"):
    """
    :param room_id: Room ID
    :return: Returns the count of tickets for the given room
    """
    current_month = datetime.now().month
    if room_id == "all":
        ticket_resolved_count_month = Tickets.objects.filter(
            created_at__month=current_month, is_resolved=True, feedback=False
        ).count()

        ticket_count_month = Tickets.objects.filter(
            created_at__month=current_month, feedback=False
        ).count()

        ticket_count_week = Tickets.objects.filter(
            created_at__week=datetime.now().isocalendar()[1], feedback=False
        ).count()

        ticket_count_day = Tickets.objects.filter(
            created_at__day=datetime.now().day, feedback=False
        ).count()

        ticket_count = Tickets.objects.filter(feedback=False).count()

        positive_count = Tickets.objects.filter(feedback=True).count()
    else:
        ticket_resolved_count_month = Tickets.objects.filter(
            created_at__month=current_month,
            is_resolved=True,
            feedback=False,
            room_id=room_id,
        ).count()

        ticket_count_month = Tickets.objects.filter(
            created_at__month=current_month, feedback=False, room_id=room_id
        ).count()

        ticket_count_week = Tickets.objects.filter(
            created_at__week=datetime.now().isocalendar()[1],
            feedback=False,
            room_id=room_id,
        ).count()

        ticket_count_day = Tickets.objects.filter(
            created_at__day=datetime.now().day, feedback=False, room_id=room_id
        ).count()

        ticket_count = Tickets.objects.filter(feedback=False, room_id=room_id).count()

        positive_count = Tickets.objects.filter(feedback=True, room_id=room_id).count()

    return {
        "ticket_count": ticket_count,
        "ticket_count_day": ticket_count_day,
        "ticket_count_week": ticket_count_week,
        "ticket_count_month": ticket_count_month,
        "ticket_resolved_count_month": ticket_resolved_count_month,
        "positive_count": positive_count,
    }
