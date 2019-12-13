from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('grant_types/', views.grant_types_list, name='grants'),
    path('grant_types/<int:pk>/', views.grants_list, name='grants_list'),
    path('grant/<int:pk>/', views.grant_detailed, name='grant_detailed'),
    path('fcp_types/', views.fcp_types_list, name='fcps'),
    path('fcp_types/<int:pk>/', views.fcps_list, name='fcps_list'),
    path('fcp/<int:pk>/', views.fcp_detailed, name='fcp_detailed'),
    path('fz44_types/', views.fz44_types_list, name='fz44s'),
    path('fz44_types/<int:pk>/', views.fz44_list, name='fz44_list'),
    path('fz44/<int:pk>/', views.fz44_detailed, name='fz44_detailed'),
    path('fz223_types/', views.fz223_types_list, name='fz223s'),
    path('fz223_types/<int:pk>/', views.fz223_list, name='fz223_list'),
    path('fz223/<int:pk>/', views.fz223_detailed, name='fz223_detailed'),
]
