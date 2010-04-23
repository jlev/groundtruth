from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render_to_response,get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.template import RequestContext

from django.views.decorators.cache import cache_page
from django.utils import simplejson as json
from django.contrib.contenttypes.models import ContentType

from django.contrib.gis.gdal import SpatialReference
from django.contrib.gis.geos import Polygon

from django.contrib.gis.shortcuts import render_to_kml

from geo.models import Barrier,Settlement,Palestinian,Checkpoint,Region
from info.models import Citation
from geo.models import geojson_base

SPHERICAL_MERCATOR = SpatialReference('EPSG:900913')
ISRAEL_TM = SpatialReference('EPSG:2039')
LAT_LON = SpatialReference('EPSG:4326')

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

@cache_page(15*60)
def kml_view(request,model_name,id):
    try:
        model_class = ContentType.objects.get(model=model_name).model_class()
    except ObjectDoesNotExist,e:
        return HttpResponse('no content exists for the model named [%s]}' % model_name)

    if id.lower() == 'all':
        objects = model_class.objects.filter().kml()
    else:
        objects = model_class.objects.filter(pk=id).kml()
    
    places = []
    for o in objects:
        p = {}
        if model_name == "settlement":
            p['name'] = o.name
            p['description'] =  "Settlement Type: %s \n" % o.get_settlement_type_display()
            if o.info: p['description'] += ('Description: %s \n' % o.info)
            if o.population:
                pop = o.most_recent_population()
                p['description'] += ('Population: %s (%s)\n' % (pop[0],pop[1]))
            if o.year_founded: p['description'] += ('Year Founded: %s \n' % o.year_founded)
            if o.year_founded: p['description'] += ('Region: %s \n' % o.region)
            b = o.boundary.transform(LAT_LON,True) #have to transform boundary kml explicitly
            p['kml'] = b.kml
            p['style'] = 'settlement'
        if model_name == "palestinian":
            p['name'] = o.name
            p['description'] = "Palestinian Area: %s\n" % o.name
            if o.population:
                pop = o.most_recent_population()
                p['description'] += ('Population: %s (%s)\n' % (pop[0],pop[1]))
            b = o.boundary.transform(LAT_LON,True)
            p['kml'] = b.kml
            p['style'] = 'palestinian'
        if model_name == "barrier":
            p['description'] = "%s\n%s" % (o.get_makeup_display(),o.get_construction_display())
            b = o.path.transform(LAT_LON,True) #have to transform boundary kml explicitly
            p['kml'] = b.kml
            p['style'] = 'barrier'
        if model_name == "border":
            b =  o.path.transform(LAT_LON,True) #have to transform boundary kml explicitly
            p['kml'] = b.kml
            p['style'] = 'border'
        if model_name == "checkpoint":
            p['name'] = o.name
            p['description'] = "%s\n%s" % (o.get_checkpoint_type_display(),o.get_direction_display())
            b = o.coords.transform(LAT_LON,True) #have to transform boundary kml explicitly
            p['kml'] = b.kml
            p['style'] = 'checkpoint'
        places.append(p)
    
    return render_to_kml("output.kml", {'places' : places, 'name':model_name})
    #return HttpResponse("not yet implemented")
    
def shapefile_view(request,model_name):
    return HttpResponse("not yet implemented")
    
def search(request):
    '''Search for a settlement or Palestinian town by name.
    Returns a list of results for jquery autocomplete'''
    try:
        query = request.GET['q']
    except KeyError:
        return HttpResponse("No query string", mimetype='text/plain')
    settlements = Settlement.objects.filter(name__istartswith=query)
    settlements_alternate = Settlement.objects.filter(alternate_name__istartswith=query)
    print settlements_alternate
    
    palestinian = Palestinian.objects.filter(name__istartswith=query)
    
    r = []
    if len(settlements) > 0:
        r.append("<div class='ac_header'>Settlements</div>")
    for s in settlements:
        geo = geojson_base(SPHERICAL_MERCATOR,s.center,{'name':str(s.name),'id':s.id})
        r.append("%s|%s|%s" % (s.name,s.get_absolute_url(),json.dumps(geo)))
    for s in settlements_alternate:
        geo = geojson_base(SPHERICAL_MERCATOR,s.center,{'name':str(s.name),'id':s.id})
        r.append("%s, (%s)|%s|%s" % (s.name,s.alternate_name,s.get_absolute_url(),json.dumps(geo)))
    if len(palestinian) > 0:
        r.append("<div class='ac_header'>Palestinian Areas</div>")
        for p in palestinian:
            geo = geojson_base(SPHERICAL_MERCATOR,p.center,{'name':str(p.name),'id':p.id})
            r.append("%s|%s|%s" % (p.name,p.get_absolute_url(),json.dumps(geo)))
    return HttpResponse('\n'.join(r), mimetype='text/plain')
    
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
    geo = geojson_base(SPHERICAL_MERCATOR,s.center,{'name':str(s.name),'id':s.id})
    return render_to_response('settlement_page.html',
        dict(settlement=s,citations=c,geojson=json.dumps(geo)),
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
    return render_to_response('region_page.html',
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
