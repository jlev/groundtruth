from django.conf import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('groundtruth.geo.views',
    (r'^$','map'),
    (r'(?P<model_name>[\w-]+)/(?P<id>\d+)/json/$','json_view'),
    (r'(?P<model_name>[\w-]+)/json/$','json_view',{'id':'all'}),
    (r'(?P<model_name>[\w-]+)/kml/$','kml_view'),
    (r'(?P<model_name>[\w-]+)/shapefile/$','shapefile_view'),
    (r'settlement/search/(?P<name>[\w\s-]+)/$','settlement_search_by_name'),
    (r'settlement/$','settlements_list'),
    (r'settlement/(?P<id>\d+)/$','settlement_page'),
    (r'settlement/(?P<id>\d+)/popup/$','settlement_popup'),
    (r'settlement/(?P<id>\d+)/edit/$','settlement_form'),
    (r'checkpoint/$','checkpoints_list'),
    (r'checkpoint/(?P<id>\d+)/$','checkpoint_page'),
    (r'checkpoint/(?P<id>\d+)/popup/$','checkpoint_popup'),
    (r'checkpoint/(?P<id>\d+)/edit/$','checkpoint_form'),
    (r'barrier/(?P<id>\d+)/popup/$','barrier_popup'),
)

urlpatterns += patterns('groundtruth.info.views',
    (r'(?P<model_name>[\w-]+)/info/$','info_popup_view'),
)

#let django serve the static media when in debug mode
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    )