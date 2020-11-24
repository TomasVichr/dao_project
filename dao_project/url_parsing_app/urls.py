from django.urls import path
from . import views

urlpatterns = [
    path('', views.ParseURLAjax.as_view()),
    path("gd/", views.GetData.as_view()),
]
