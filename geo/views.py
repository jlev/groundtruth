from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render_to_response,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

from django.views.decorators.cache import cache_page
from django.utils import simplejson as json
from django.contrib.contenttypes.models import ContentType

from django.contrib.gis.gdal import SpatialReference
from django.contrib.gis.geos import Polygon

from geo.models import Barrier,Settlement,Palestinian,Checkpoint,Region
from info.models import Citation
from geo.models import geojson_base

SPHERICAL_MERCATOR = SpatialReference('EPSG:900913')

def map(request):
    lat = request.GET.get('lat', '') 
    lon = request.GET.get('lng', '')
    zoom = request.GET.get('zoom', '')
    return render_to_response('map.html',
        dict(lat=lat,lon=lon,zoom=zoom),
        context_instance = RequestContext(request))
    
def iframe(request):
    lat = request.GET.get('lat', '') 
    lon = request.GET.get('lng', '')
    zoom = request.GET.get('zoom', '')
    return render_to_response('iframe.html',
        dict(lat=lat,lon=lon,zoom=zoom),
        context_instance = RequestContext(request))

@cache_page(15*60)
def json_view(request,model_name,id):
    '''Generic view for geojson view of a GeoModel derived class'''
    try:
        model_class = ContentType.objects.get(model=model_name).model_class()
    except ObjectDoesNotExist,e:
        return HttpResponse('{name: "JSONRequestError", message: "no content exists for the model named [%s]}"' % model_name)
    #if not isinstance(model_class,GeoModel):
        #FIXME: this returns false even when using django subclasses
    #    return HttpResponse("{Error: view undefined for class named [%s]}" % model_name)
    
    obj = {}
    obj['type']='FeatureCollection'
    features = []
    if id.lower() == 'all':
        query = model_class.objects.filter()
    else:
        query = model_class.objects.filter(pk=id)
    #create the json strings, if they don't already exist
    query.geojson(precision=2,bbox=True,crs=True)
    for s in query:
        features.append(s.get_geojson_dict(SPHERICAL_MERCATOR))
        #fixme, pass srid in through url
    obj['features'] = features
    return HttpResponse(json.dumps(obj))

def kml_view(request,model_name):
    return HttpResponse("not yet implemented")
    
def shapefile_view(request,model_name):
    return HttpResponse("not yet implemented")
    
def settlement_search_by_name(request,name):
    '''Search for a settlement by name.
    Returns a geojson object of results'''
    #TODO: make this compatible with CloudMade search API, so we can use interchangeably
    matches = Settlement.objects.filter(name__icontains=name)
    #should use search, but not implemented for postgres
    if len(matches) == 0:
        return HttpResponseNotFound("No Settlement found by that name")
        #better error handling
        #transliteration?

    matches.geojson(precision=2,crs=True)
    #attach geojson attributes
    obj = {}
    obj['query']=name
    obj['type']='FeatureCollection'
    features = []
    for s in matches:
        #only return the center point, not the whole border
        #reduced_geojson_dict = geojson_base(s.center,{'name':str(s.name),'id':s.id})
        #features.append(reduced_geojson_dict)
        #
        features.append(s.get_geojson_dict(SPHERICAL_MERCATOR))
    obj['features'] = features
    bounds = Polygon.from_bbox(matches.extent())
    bounds.srid = 2039
    bounds.transform(SPHERICAL_MERCATOR)
    obj['bounds'] = bounds.extent
    return HttpResponse(json.dumps(obj))
    
def settlement_popup(request,id):
    s = get_object_or_404(Settlement,pk=id)
    return render_to_response('settlement_popup.html',
        dict(settlement=s),
        context_instance = RequestContext(request))
        
def settlements_list(request):
    s = Settlement.objects.all()
    return render_to_response('settlements_list.html',
        dict(settlements=s),
        context_instance = RequestContext(request))

def settlement_page(request,id):
    s = get_object_or_404(Settlement,pk=id)
    c = Citation.objects.filter(model__name="settlement")
    return render_to_response('settlement_page.html',
        dict(settlement=s,citations=c),
        context_instance = RequestContext(request))


def palestinian_page(request,id):
    p = get_object_or_404(Palestinian,pk=id)
    c = Citation.objects.filter(model__name="palestinian")
    return render_to_response('palestinian_page.html',
        dict(town=p,citations=c),
        context_instance = RequestContext(request))

def palestinian_popup(request,id):
    t = get_object_or_404(Palestinian,pk=id)
    return render_to_response('palestinian_popup.html',
        dict(town=t),
        context_instance = RequestContext(request))

def settlement_form(request,id):
    #TODO
    return HttpResponse("not yet implemented")

def region_page(request,id):
    r = get_object_or_404(Region,pk=id)
    s = Settlement.objects.filter(region__id=id)
    return render_to_response('geo/region_page.html',
        dict(region=r,settlements=s),
        context_instance = RequestContext(request))

def region_list(request):
    r = Region.objects.all()
    return render_to_response('region_list.html',
        dict(regions=r),
        context_instance = RequestContext(request))
  
def barrier_popup(request,id):
    b = get_object_or_404(Barrier,pk=id)
    return render_to_response('barrier_popup.html',
        dict(barrier=b),
        context_instance = RequestContext(request))

def checkpoint_popup(request,id):
    c = get_object_or_404(Checkpoint,pk=id)
    return render_to_response('checkpoint_popup.html',
        dict(checkpoint=c),
        context_instance = RequestContext(request))

def checkpoints_list(request):
    c = Checkpoint.objects.all()
    return render_to_response('checkpoints_list.html',
        dict(checkpoints=c),
        context_instance = RequestContext(request))

def checkpoint_page(request,id):
    c = get_object_or_404(Checkpoint,pk=id)
    return render_to_response('checkpoint_page.html',
        dict(checkpoint=c),
        context_instance = RequestContext(request))

def checkpoint_form(request,id):
    #TODO
    return HttpResponse("not yet implemented")
