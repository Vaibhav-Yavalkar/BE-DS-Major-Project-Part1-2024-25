from django.urls import path
from .models import *
from .views import *

# Create your views here.
urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('<int:alert>/', Index.as_view(), name='index'),
    path('api/alerts/', AlertView.as_view(), name='alert'),
]