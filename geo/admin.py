from django.contrib import admin
from olwidget.admin import GeoModelAdmin
import geo.models

class GenericGeoAdmin(GeoModelAdmin):
    options= {
        'layers':['osm.mapnik','google.hybrid']
    }

class SettlementGeoAdmin(GenericGeoAdmin):
    list_display = ('name','alternate_name','hebrew_name','region','settlement_type','year_founded')
    search_fields = ['name']
#    fieldsets = (
#           ('Information', {
#               'fields': ('name','alternate_name','hebrew_name','region','settlement_type','year_founded','area','population')
#           }),
#           ('Geography', {
#               'fields': ('boundary')
#           }),
#       )
#            ('Extra', {
#                'classes': ('collapse'),
#                'fields': ('center')
#            }),
#        )

class PalestinianGeoAdmin(GenericGeoAdmin):
    list_display = ('name','arabic_name')
    search_fields = ['name']
#    fieldsets = (
#            ('Information', {
#                'fields': ('name', 'arabic_name','area', 'population')
#            }),
#            ('Geography', {
#                'fields': ('boundary')
#            }),
#            ('Extra', {
#                'classes': ('collapse'),
#                'fields': ('center')
#            }),
#        )
    
admin.site.register(geo.models.Settlement,SettlementGeoAdmin)
admin.site.register(geo.models.Palestinian,PalestinianGeoAdmin)
admin.site.register(geo.models.Region,GenericGeoAdmin)
admin.site.register(geo.models.Barrier,GenericGeoAdmin)
admin.site.register(geo.models.Border,GenericGeoAdmin)
admin.site.register(geo.models.Checkpoint,GenericGeoAdmin)