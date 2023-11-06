from django.contrib import admin
from django.urls import path, include
from points.views import index_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view),
    path('points/', include("points.api.urls"))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
