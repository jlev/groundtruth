from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

CITABLE_MODELS = {"model__in": ("settlement","region","barrier","checkpoint","border",
                                "company","product")}
GEO_MODELS = {"model__in": ("settlement","region","barrier","checkpoint","border")}

class Source(models.Model):
    '''A name, url and date'''
    name = models.CharField('Name',max_length=50)
    author = models.CharField('Author',max_length=50,null=True,blank=True)
    url = models.URLField(null=True,blank=True)
    date = models.DateField(auto_now=False,null=True,blank=True)
    def __unicode__(self):
        return self.name

class Citation(models.Model):
    '''Link a specific field in a particular model to a source'''
    source = models.ForeignKey(Source)
    cited_type = models.ForeignKey(ContentType,limit_choices_to=CITABLE_MODELS)
    cited_field = models.CharField(max_length=25,blank=True,null=True)
    cited_id = models.PositiveIntegerField(default=0)
    cited_object = GenericForeignKey("cited_type","cited_id")
    def __unicode__(self):
        if self.cited_id == 0:
            object_name = self.cited_type
        else:
            object_name = cited_object #self.model.get_object_for_this_type(id=self.cited_id)
        return '%s: %s %s' % (self.source.name,object_name,self.cited_field)

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