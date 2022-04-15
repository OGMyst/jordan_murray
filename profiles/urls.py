from django.urls import path
from .views import ProfilePageView, ProfileAdminPageView

urlpatterns = [
    path('<section>', ProfilePageView.as_view()),
    path('admin/<section>', ProfileAdminPageView.as_view()),
]
