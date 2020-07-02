from django.urls import path
from . import views 

app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:slug>/', views.details, name='details'),
    path('<str:slug>/inscricao/', views.enrollment, name='enrollment'),

]