from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('pages.urls')),
    path('http/', include('pages.httpbin_scenarios.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
