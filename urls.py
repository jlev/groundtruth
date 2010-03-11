from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

#admin urls
urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls))
)

#tagging urls
#urlpatterns += patterns('',
#    (r'^autocomplete/', include('autocomplete.urls'))
#)

#app urls
urlpatterns += patterns('',
    (r'', include('info.urls')),
    (r'', include('geo.urls')),
)

#let django serve the static media when in debug mode
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    )
