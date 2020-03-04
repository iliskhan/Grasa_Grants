from django.urls import path, include
#from main import main_views
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url


urlpatterns = [
    path('signup/', views.signup, name = 'signup'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('', include ('django.contrib.auth.urls') ),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]