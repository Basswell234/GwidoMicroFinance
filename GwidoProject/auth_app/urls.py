from django.urls import include, path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
]
