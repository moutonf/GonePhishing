
from django.conf.urls import url,include
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('services.urls')),
    url(r'^index/$', include('services.urls')),
    url(r'^loggedin/in/$', include('services.urls')),
]
