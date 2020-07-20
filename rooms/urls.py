from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("list", views.ListRoomsView.as_view()),
    path("<int:primary_key>/", views.SeeRoomView.as_view()),
]

