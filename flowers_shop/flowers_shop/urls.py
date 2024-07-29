from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('catalog/', include('catalog.urls')),
    path('orders/', include('orders.urls')),
    path('reviews/', include('reviews.urls')),
    path('analytics/', include('analytics.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
