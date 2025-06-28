from django.urls import path
from . import views

urlpatterns = [
    path('status/<int:code>/', views.status_code, name='status_code'),
    path('redirect/', views.redirect, name='redirect'),
    path('redirect/<int:count>/', views.redirect_chain, name='redirect_chain'),
    path('headers/', views.headers, name='headers'),
    path('cookies/', views.cookies, name='cookies'),
    path('cookies/set/<str:name>/<str:value>/', views.cookies_set, name='cookies_set'),
    path('cookies/delete/<str:name>/', views.cookies_delete, name='cookies_delete'),
    path('json/', views.json_response, name='json_response'),
    path('xml/', views.xml_response, name='xml_response'),
    path('base64/<str:encoded_string>/', views.base64_decode, name='base64_decode'),
    path('html/', views.html_response, name='html_response'),
    path('robots.txt/', views.robots_txt, name='robots_txt'),
    path('user-agent/', views.user_agent, name='user_agent'),
    path('ip/', views.ip_address, name='ip_address'),
    path('get/', views.get_request, name='get_request'),
    path('post/', views.post_request, name='post_request'),
    path('anything/', views.anything_request, name='anything_request'),
]
