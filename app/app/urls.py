from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url('', include('auth.urls')),
        url('calculimc/', include('calculimc.urls')),
        url('calculdej/', include('calculdej.urls')),
        url('consulterdossier/', include('consulterdossier.urls')),
        url('consultertouslesdossiers/', include('consultertouslesdossiers.urls')),
        url(r'^captcha/', include('captcha.urls')),
]
