from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('disease-prediction/', views.disease_prediction, name='disease_prediction'),
    path('forecast-analysis/', views.forensics_analysis, name='forensics_analysis'),
    path('about-author/', views.about_author, name='about_author'),
    path('faqs/', views.faqs, name='faqs'),
]
