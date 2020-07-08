from django.urls import path
from . import views 

app_name = 'courses'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:slug>/', views.details, name='details'),
    path('<str:slug>/inscricao/', views.enrollment, name='enrollment'),
    path('<str:slug>/anuncios/', views.announcements, name='announcements'),
    path('<str:slug>/cancelar-inscricao/', views.undo_enrollment, name='undo_enrollment'),
    path('<str:slug>/anuncios/<int:pk>', views.show_announcement, name='show_announcement'),
    path('<str:slug>/aulas/', views.lessons, name='lessons'),
    path('<str:slug>/aulas/<int:pk>/', views.lesson, name='lesson'),
    path('<str:slug>/materiais/<int:pk>/', views.material, name='material'),

]