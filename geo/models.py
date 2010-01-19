from django.contrib.gis.db import models
from fields import JSONField

#EPSG codes
ISRAEL_TM = 2039
SPHERICAL_MERCATOR = 900913

def geojson_base(projection,the_geom,properties):
    '''Returns a geojson compatible dictionary, with coords from geom_field in the specified projection.
    Note that to you still have to turn this into real json with dumps()
    Pass in the geometry field, and a properties dictionary
    Follows GeoJSON 1.0 spec: http://geojson.org/geojson-spec.html'''
    dic = {}
    dic['type']='Feature'
    the_geom.transform(projection) #convert to output proj, works in place but doesn't save to db
    dic['geometry']=eval(the_geom.geojson) #eval is necessary to get rid of string notation    
    dic['properties'] = properties
    #create reference system
    dic['crs'] = {'type':'name','properties':{'name':'EPSG:%s' % projection.srid}}
    return dic

class Settlement(models.Model):
    name = models.CharField('Name',max_length=50)
    alternate_name = models.CharField('Alternate Names',max_length=100,null=True,blank=True)
    region = models.ForeignKey('Region',blank=True,null=True)
    info = models.TextField('General Information',null=True,blank=True)
    legal = models.TextField('Legal Information',null=True,blank=True)
    area = models.IntegerField('Area in square km',null=True,blank=True)
    population = JSONField('Population',null=True,blank=True)
    SETTLEMENT_TYPE_CHOICES = (
        ('STL','Settlement'),
        ('EJS','East Jerusalem'),
        ('OUT','Outpost'),
        ('IND','Industrial Area'),
        ('MIL','Military Base')
    ) #The long forms match the data from the shapefiles
    settlement_type = models.CharField('Type of Settlement',max_length=3,choices=SETTLEMENT_TYPE_CHOICES)
    year_founded = models.CharField(max_length=4,null=True,blank=True)
    evacuated = models.BooleanField(default=False)
    #geographic fields
    center = models.PointField(srid=ISRAEL_TM,null=True,blank=True)
    boundary = models.MultiPolygonField(srid=ISRAEL_TM)
    built_up = models.MultiPolygonField(srid=ISRAEL_TM,null=True,blank=True)
    objects = models.GeoManager()
    
    def most_recent_population(self):
        "returns the most recent population and year"
        years = sorted(self.population.keys())
        latest = years[-1]
        pop = self.population[latest]
        return (pop,latest)
    def population_chartstring(self):
        "returns a flot chart variable from a dictionary"
        years = sorted(self.population.keys())
        var = []
        for y in years:
            var.append([int(y),int(self.population[y])])
        return var
    def get_geojson_dict(self,projection):
        self.center.transform(projection)
        return geojson_base(projection,self.boundary,
                            {'name':str(self.name),
                              'id':self.id,
                              'center':eval(self.center.geojson)
                          })
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return "/settlement/%i/" % self.id

    def save(self):
        self.center = self.boundary.centroid
        self.save_base(force_insert=False, force_update=False)
    class Meta:
        ordering = ['name']

class Region(models.Model):
    #Also known as settlement bloc
    name = models.CharField('Name',max_length=50)
    boundary = models.MultiPolygonField(srid=ISRAEL_TM,null=True,blank=True)
    objects = models.GeoManager()
    def get_geojson_dict(self,projection):
           return geojson_base(projection,
                               self.boundary,
                               {'name':self.name,
                               'id':self.id})
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return "/region/%i/" % self.id

class Barrier(models.Model):
    BARRIER_MAKEUP_CHOICES = (
        ('WALL','Wall'),
        ('FENCE','Fence'),
        ('UNKWN','Unknown')
    )
    makeup = models.CharField(max_length=5,choices=BARRIER_MAKEUP_CHOICES)
    BARRIER_CONTRUCTION_CHOICES = (
        ('PLAN','Planned'),
        ('UNDER','Under Construction'),
        ('COMPL','Completed'),
        ('ROAD','Road Protection'),
        ('FURTH','Subject to Further Inter-Ministerial Examination'),
        ('DISM','Dismantled'),
    ) #The long forms match the fields from barrier shapefile
    construction = models.CharField(max_length=5,choices=BARRIER_CONTRUCTION_CHOICES)
    path = models.MultiLineStringField(srid=ISRAEL_TM)
    objects = models.GeoManager()
    def __unicode__(self):
        return "%i - %s" % (self.id,self.makeup)
    def get_geojson_dict(self,projection):
        return geojson_base(projection,self.path,
                            {"construction":self.get_construction_display(),'id':self.id})
    
class Border(models.Model):
    name = models.CharField(max_length=100)
    path = models.MultiLineStringField(srid=ISRAEL_TM)
    objects = models.GeoManager()
    
    def get_geojson_dict(self,projection):
        return geojson_base(projection,self.path,{})
    def __unicode__(self):
        return self.name

class Checkpoint(models.Model):
    name = models.CharField('Name',max_length=50,null=True)
    region = models.CharField('Name of the Region',max_length=50,null=True)
    CHECKPOINT_TYPE_CHOICES = (
        ('CKPT','Checkpoint'),
        ('HCKPT','HCheckpoint'),
        ('PART','Partial Checkpoint'),
        ('MOUND','Earthmound'),
        ('OBSRV','Observation Tower'),
        ('BLOCK','Road Block'),
        ('RGATE','Road Gate'),
        ('AGATE','Agricultural Gate'),
        ('TUNNL','Tunnel'),
        ('PTUNL','Planned Tunnel'),
        ('DCO','DCO')
    )
    checkpoint_type = models.CharField(max_length=5,choices=CHECKPOINT_TYPE_CHOICES)
    CHECKPOINT_DIRECTION_CHOICES = (
        ('TOISR','To Israel'),
        ('INNER','Inner'),
        ('HBRON','Hebron Inner'),
        ('UNKWN','Unknown')
    )
    direction = models.CharField(max_length=5,choices=CHECKPOINT_DIRECTION_CHOICES)
    staffed = models.NullBooleanField()
    coords = models.PointField(srid=ISRAEL_TM)
    objects = models.GeoManager()
    
    def __unicode__(self):
        if not (self.name.isspace() or self.name == ""):
            return self.name
        else:
            return "Unnamed Checkpoint"
    def get_absolute_url(self):
        return "/checkpoint/%i/" % self.id


    def get_geojson_dict(self,projection):
        return geojson_base(projection,self.coords,
                            {'name':self.name,
                            'type':self.get_checkpoint_type_display(),
                            'id':self.id})
