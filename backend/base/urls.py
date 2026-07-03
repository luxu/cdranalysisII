from django.urls import path

from cdranalysis.base import views

urlpatterns = [
    path('', views.home, name='home'),
]
