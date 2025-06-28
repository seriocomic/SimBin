from django.urls import path, re_path
from django.views.generic.base import RedirectView
from pages import views

urlpatterns = [
    path('favicon.ico/', RedirectView.as_view(url='/static/favicon.ico')),
    path('robots.txt', views.robots, name='robots'),
    re_path(r'^(?P<url>.*)/$', views.handle, name='handle'),
    path('', views.index, name='index'),
]
