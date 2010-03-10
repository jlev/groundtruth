from django.contrib import admin
from django import forms
from info.models import Source,Citation,LayerInfo
from info.forms import CitationForm

class CitationAdmin(admin.ModelAdmin):
    form = CitationForm

admin.site.register(Source)
admin.site.register(Citation,CitationAdmin)
admin.site.register(LayerInfo)