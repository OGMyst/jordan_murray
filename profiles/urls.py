from django.urls import path
from .views import ProfilePageView

urlpatterns = [
    path('<section>', ProfilePageView.as_view()),
]
