from django.db import models
from django.contrib.contenttypes.models import ContentType

GEO_MODELS = {"model__in": ("settlement","region","barrier","checkpoint","border","palestinian")}

class Source(models.Model):
    '''A name, url and date'''
    name = models.CharField('Name',max_length=50)
    url = models.URLField()
    date = models.DateField(null=True,blank=True)
    def __unicode__(self):
        return self.name

class Citation(models.Model):
    '''The source for a specific field in a geo model'''
    source = models.ForeignKey(Source)
    model = models.ForeignKey(ContentType,limit_choices_to=GEO_MODELS)
    field = models.CharField(max_length=25,blank=True,null=True) #limited in CitationAdmin
    #object_id = models.PositiveIntegerField()
    def __unicode__(self):
        return '%s: %s %s' % (self.source.name,self.model,self.field)
    def field_choices(self):
        '''Limits field choices to those available for the given model'''
        model_class = self.model.model_class()
        model_fields = model_class._meta._fields() #uses internal api, but should continue to work
        model_fields.pop(0) #drop the pk
        r = []
        for f in model_fields:
            r.append(f.name)
        return r
    
class LayerInfo(models.Model):
    '''Description for each model type in the geo application'''
    content_type = models.ForeignKey(ContentType,limit_choices_to=GEO_MODELS,unique=True)
    citations = models.ManyToManyField(Citation,null=True,blank=True)
    description = models.TextField()
    downloadable = models.BooleanField(default=True)

    def __unicode__(self):
        return self.content_type.name
    class Meta:
        verbose_name = "layer"
        verbose_name_plural = "Layer Info"