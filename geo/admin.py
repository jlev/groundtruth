from django.contrib import admin
from olwidget.admin import GeoModelAdmin

from models import Settlement,Region,Border,Barrier,Checkpoint

class SettlementGeoAdmin(GeoModelAdmin):
    list_display = ('name','alternate_name','region','settlement_type','year_founded')
    search_fields = ['name']
    options= {
        'layers':['osm.mapnik']
    }

class GenericGeoAdmin(GeoModelAdmin):
    options= {
        'layers':['osm.mapnik']
    }

admin.site.register(Settlement,SettlementGeoAdmin)
admin.site.register(Region,GenericGeoAdmin)
admin.site.register(Barrier,GenericGeoAdmin)
admin.site.register(Border,GenericGeoAdmin)
admin.site.register(Checkpoint,GenericGeoAdmin)