from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.dashboard_login, name='dashboard_login'),
    path('logout/', views.dashboard_logout, name='dashboard_logout'),
    path('', views.dashboard_index, name='dashboard_index'),
    path('<path:subpath>/', views.dashboard_index, name='dashboard_spa'),
]
