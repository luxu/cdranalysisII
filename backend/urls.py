from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('cdranalysis.base.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
