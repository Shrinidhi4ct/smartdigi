"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from .views.dashbaord import *
from .views.reasons import *
from .views.checklist import *
from .views.floors import *
from .views.rooms import *
from .views.user import *
from .views.maintenance import *
from .views.rating import *
from .views.reports import *
from .views.alerts import *
from .views.charts_view import *


urlpatterns = [
    path("", TicketDashboardView.as_view(), name="dashboard"),
    path("iaq/", IAQDashboardView.as_view(), name="iaq_dashboard"),
    path(
        "room_ticket_dashboard/<int:pk>/",
        RoomDashboardView.as_view(),
        name="room_dashboard",
    ),
    path(
        "room_iaq_dashboard/<int:pk>/",
        RoomIAQDashboardView.as_view(),
        name="room_iaq_dashboard",
    ),
    # reason List
    path("reasons/", ReasonListView.as_view(), name="reason_list"),
    # Reason Create
    path("reasons/create/", ReasonCreateView.as_view(), name="reason_create"),
    # Reason Update
    path("reasons/<int:pk>/update/", ReasonUpdateView.as_view(), name="reason_update"),
    # Reason Delete
    path("reasons/<int:pk>/delete/", ReasonDeleteView.as_view(), name="reason_delete"),
    # Check List
    path("check_list/", CheckListView.as_view(), name="check_list"),
    # Check list create
    path("check_list/create", CheckListCreateView.as_view(), name="check_list_create"),
    # Check list update
    path(
        "check_list/<int:pk>/update",
        CheckListUpdateView.as_view(),
        name="check_list_update",
    ),
    # Check list delete
    path(
        "check_list/<int:pk>/delete",
        CheckListDeleteView.as_view(),
        name="check_list_delete",
    ),
    # Floor List
    path("floors/", FloorListView.as_view(), name="floor_list"),
    # Floor Create
    path("floors/create/", FloorCreateView.as_view(), name="floor_create"),
    # Floor Update
    path("floors/<int:pk>/update/", FloorUpdateView.as_view(), name="floor_update"),
    # Floor Delete
    path("floors/<int:pk>/delete/", FloorDeleteView.as_view(), name="floor_delete"),
    # Room List
    path("rooms/", RoomListView.as_view(), name="room_list"),
    # Room Create
    path("rooms/create/", RoomCreateView.as_view(), name="room_create"),
    # Room Update
    path("rooms/<int:pk>/update/", RoomUpdateView.as_view(), name="room_update"),
    # Room Delete
    path("rooms/<int:pk>/delete/", RoomDeleteView.as_view(), name="room_delete"),
    # User List
    path("users/", UserListView.as_view(), name="user_list"),
    # User Create
    path("users/create/", UserCreateView.as_view(), name="user_create"),
    # User Update
    # path("users/<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
    # User Delete
    path("users/<int:pk>/delete/", UserDeleteView.as_view(), name="user_delete"),
    # Maintenance
    path(
        "maintenance/", MaintenaceDashboardView.as_view(), name="maintenance_dashboard"
    ),
    # Maintenance Ticket Update
    path(
        "maintenance/<int:pk>/update/",
        MaintenanceTicketUpdateView.as_view(),
        name="maintenance_ticket_update",
    ),
    # Maintenance Ticket View By Room
    path(
        "maintenance/<int:pk>/",
        MaintenanceTicketByRoomView.as_view(),
        name="maintenance_ticket_by_room", 
    ),
    # rating list
    path("rating/", RatingListView.as_view(), name="rating_list"),
    # rating create
    path("rating/create/", RatingCreateView.as_view(), name="rating_create"),
    # rating update
    path("rating/<int:pk>/update/", RatingUpdateView.as_view(), name="rating_update"),
    # rating delete
    path("rating/<int:pk>/delete/", RatingDeleteView.as_view(), name="rating_delete"),
    # Reports
    path("reports/", ReportGeneralView.as_view(), name="reports"),
    # alerts
    path("alerts/", AlertConditionsView.as_view(), name="alerts"),
    # heatmap
    path("heatmap/<str:pk>", HeatMapDataView.as_view(), name="heatmap"),
    # linechart
    path("linechart/<str:pk>", LineChartDataView.as_view(), name="linechart"),
    # Linechart all
    path("linechart_all/", LineChartFullDataView.as_view(), name="linechart_all")
]
