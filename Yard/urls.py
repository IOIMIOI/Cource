from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

from Yard import settings
from user.views import pageNotFound

from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('', include('file.urls')),
    path('chat/', include('chat.urls')),
    path('poll/', include('poll.urls')),



]
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
