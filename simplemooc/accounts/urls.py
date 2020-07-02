from django.urls import path, include
from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('', include('django.contrib.auth.urls'), name='login'),
    path('cadastre-se/', views.register, name='register'),
    path('nova-senha/', views.password_reset, name='password_reset'),
    path('confirmar-nova-senha/<str:key>', views.password_reset_confirm, name='password_reset_confirm'),
    path('editar/', views.edit, name='edit'),
    path('senha/', views.edit_password, name='edit_password'),

]