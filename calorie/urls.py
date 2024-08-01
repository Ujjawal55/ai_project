from django.urls import path
from calorie import views

urlpatterns = [
    path("", views.upload_view, name="homePage"),
    path("result/<str:file_name>", views.result_view, name="result"),
]
