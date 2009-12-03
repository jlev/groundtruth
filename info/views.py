from django.http import HttpResponse,HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import render_to_response,get_object_or_404

from info.models import LayerInfo,Source,Citation

def info_popup_view(request,model_name):
    l = get_object_or_404(LayerInfo,content_type__name=model_name)
    name=l.content_type.name
    citations = l.citations.select_related()
    return render_to_response('info/layer_popup.html',
        dict(layer=l,name=name,citations=citations),
        context_instance = RequestContext(request))
        
def osm_popup_view(request):
    return HttpResponse("not yet implemented")