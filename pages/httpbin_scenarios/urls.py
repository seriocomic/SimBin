from django.urls import path
from . import views

urlpatterns = [
    path('status/<int:code>/', views.status_code, name='status_code'),
    path('redirect/', views.redirect, name='redirect'),
    path('headers/', views.headers, name='headers'),
    path('cookies/', views.cookies, name='cookies'),
    path('json/', views.json_response, name='json_response'),
    path('xml/', views.xml_response, name='xml_response'),
    path('base64/<str:encoded_string>/', views.base64_decode, name='base64_decode'),
    path('html/', views.html_response, name='html_response'),
    path('robots.txt/', views.robots_txt, name='robots_txt'),
]
