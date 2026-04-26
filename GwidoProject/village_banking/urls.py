from django.urls import include, path
from . import views

urlpatterns = [
    path('investment/', views.investment, name='investment'),
]
