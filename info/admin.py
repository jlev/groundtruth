from django.contrib import admin
from django import forms
from info.models import Source,Citation,LayerInfo


class CitationAdmin(admin.ModelAdmin):
    #TODO, constrain field choices to Citation.field_choices()
    pass

admin.site.register(Source)
admin.site.register(Citation,CitationAdmin)
admin.site.register(LayerInfo)