from django.urls import path
from . import views
urlpatterns = [
    path('create_ec2/', views.create_ec2, name='create_ec2')
]