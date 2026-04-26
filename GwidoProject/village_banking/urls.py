from django.urls import include, path
from . import views

urlpatterns = [
    path('investment/', views.investment, name='investment'),
    path('request_loan/', views.request_loan, name='request_loan'),
]
