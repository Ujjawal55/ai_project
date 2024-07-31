from django.urls import path
from calorie import views

urlpatterns = [
    path("", views.homePage, name="homePage"),
]
