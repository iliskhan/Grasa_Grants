from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),

    path('types/<str:tab_name>/', views.TypesList.as_view(), name='types'),
    path('types/<str:tab_name>/regions_list/', views.regions_list, name='regions_list'),
    path('types/<str:tab_name>/<int:pk>/', views.category_list, name='category_list'),
    path('detailed/<str:tab_name>/<int:pk>/', views.detailed, name='detailed'),

    path('api/suggestions/regions/', views.get_regions_api, name='suggestion_regions'),
]
