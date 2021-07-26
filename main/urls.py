from django.urls import path
from .import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("scanurl/<str:filename>/<str:token>/<str:issued>/<str:expires>/", views.ScanURLView.as_view(), name="scanurl")
]