from django.urls import path, include
from . import views
 

urlpatterns = [
    path('', views.index, name = "home"),
    path('types/<str:tab_name>/', views.TypesList.as_view(), name='types_list'),
    path('types/<str:tab_name>/regions_list/', views.regions_list, name='regions_list'),
    path('types/<str:tab_name>/<int:pk>/', views.subtypes_list, name='subtypes_list'),
    path('types/<str:tab_name>/<str:region>/', views.region_types_list, name='region_types_list'),
    path('types/<str:tab_name>/<str:region>/<int:pk>/', views.region_subtypes_list, name='region_subtypes_list'),
    path('detailed/<str:tab_name>/<int:pk>/', views.detailed, name='detailed'),

    path('favorite_post/', views.favorite_post, name='favorite_post'),
    path('favorite_list/', views.favorite_list, name='favorite_list'),

    path('subscription/', views.subscription, name='subscription'),
    path('buy_subscription/', views.buy_subscription, name='buy_subscription'),


]
