from django.urls import path, include
from .views import CustomLoginView
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    #path("login/", CustomLoginView.as_view()),
    
]