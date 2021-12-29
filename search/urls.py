from django.urls import path
from . import views
from django.conf.urls import url, include
from django.contrib.auth import login, logout
urlpatterns = [
    path('result', views.result, name='result'),
    path('home/', views.home, name='home'),
    path('', views.home, name='home'),
    path('favorite/', views.favorite, name='favorite'),
    url(r'^post/', views.for_ajax),
    path('favorite/delete/', views.delete),
    url(r'^login/$', login,
        {'template_name': 'accounts/login.html'},
        name='login'),
    url(r'^logout/$', logout, name='logout')
]
