from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf.urls.static import static

# This is used to serve the static files.
urlpatterns = staticfiles_urlpatterns()

# Serve the media files.
# urlpatterns = patterns('',) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = patterns('',
    # Examples:
    url(r'^calculate$', 'materdei.views.calculate'),
    url(r'^$', 'materdei.views.home', name='home'),
    # url(r'^materdei/', include('materdei.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
