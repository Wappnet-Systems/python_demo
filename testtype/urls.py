from django.urls import path
from .views import Testtype

app_name = 'TestType'
urlpatterns = [
    path('types/', Testtype.as_view(), name='types')
]
