from django.urls import path
from .import views

urlpatterns = [
    path("scan/<str:filename>/", views.ScanURLView.as_view(), name="scanurl"),
    path("results/<str:scan_id>/<str:access_token>", views.CheckResult.as_view(), name="results")
]