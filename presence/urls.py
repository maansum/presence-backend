
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('accounts.urls')),
    path('group/', include('groups.urls')),
    path('attendance/', include('attendances.urls')),
    path('capture/', include('process.urls')),


    ]

urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
