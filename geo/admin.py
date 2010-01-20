from django.contrib import admin
from olwidget.admin import GeoModelAdmin
import geo.models

class SettlementGeoAdmin(GeoModelAdmin):
    list_display = ('name','alternate_name','hebrew_name','region','settlement_type','year_founded')
    search_fields = ['name']
    options= {
        'layers':['osm.mapnik']
    }

class PalestinianGeoAdmin(GeoModelAdmin):
    list_display = ('name','arabic_name')
    search_fields = ['name']
    options= {
        'layers':['osm.mapnik']
}

class GenericGeoAdmin(GeoModelAdmin):
    options= {
        'layers':['osm.mapnik']
    }

admin.site.register(geo.models.Settlement,SettlementGeoAdmin)
admin.site.register(geo.models.Palestinian,PalestinianGeoAdmin)
admin.site.register(geo.models.Region,GenericGeoAdmin)
admin.site.register(geo.models.Barrier,GenericGeoAdmin)
admin.site.register(geo.models.Border,GenericGeoAdmin)
admin.site.register(geo.models.Checkpoint,GenericGeoAdmin)