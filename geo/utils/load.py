import os,csv
from geo.utils.layermapping import LayerMapping
from django.contrib.gis.gdal import DataSource
from django.db.models import Q

from geo.models import Settlement,Barrier,Checkpoint,Border,Region

def load():
    #loads all data sources in requisite order
    settlement_borders()
    built_up_areas()
    east_jerusalem()
    region_borders()
    population()
    
    checkpoints()
    barrier()
    greenline()

def settlement_borders():
    #Performs layermapping on settlement borders shapefile from PeaceNow
    mapping = {
        'name':'NameEng',
        'boundary':'Polygon',
        'settlement_type':'Type'
    }
    shape = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/settlement_borders.shp'))
    lm = LayerMapping(Settlement,shape,mapping,
                      transform=False)
                      #unique='name')
    lm.save(strict=True, verbose=True)

def built_up_areas():
    #can't use layermapping, because need to add to existing settlement objects
    #do it manually
    pass
    
def east_jerusalem():
    mapping = {
        'name':'Name',
        'boundary':'Polygon'
    }
    shape = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/jewish_east_jlsm.shp'))
    lm = LayerMapping(Settlement,shape,mapping,
                      transform=False)
                      #unique='name')
    lm.save(strict=True, verbose=True)

def region_borders():
    pass

def population():
    theFile = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/fmep-settlement-pop.txt'))
    reader = csv.DictReader(open(theFile),delimiter='\t')
    print "opened",theFile
    years = ['2008', '2007', '2006', '2005', '2004', '2003', '2002', '2001', '2000', '1999']
    for row in reader:
        name = row['Name']
        #print row
        settlement = Settlement.objects.filter(Q(name__iexact=name)|Q(alternate_name__icontains=name))
        if len(settlement) == 0:
            print "could not find settlement",name
            id = raw_input("ID of existing model: ")
            if(id == '0'):
                continue
            s = Settlement.objects.filter(pk=id)[0]
        elif len(settlement) > 1:
            print "found multiple for ",name
            for match in settlement:
                print "%i,%s\n" % (match.pk,match.name)
            id = raw_input("ID of matching model: ")
            if(id == '0'):
                continue
            s = Settlement.objects.filter(pk=id)[0]
        else:
            s = settlement[0]
        #r = Region.objects.get_or_create(name=row['Region'])
        #s.region = r
        d = {}
        for y in years:
            d[str(y)] = str(row[y])
        s.population = d
        s.year_founded = row['Date Established']
        s.save()
        print "saved",name,d

def outposts():
     #Performs layermapping on outposts shapefile from PeaceNow
        mapping = {
            'name':'Name_eng',
            'boundary':'Polygon'
        }
        shape = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/Outposts_haaretz.shp'))
        lm = LayerMapping(Settlement,shape,mapping,
                          transform=False)
                          #unique='name')
        lm.save(strict=True, verbose=True)
     
def barrier():
    #Performs layermapping on barrier shapefile from PeaceNow
    mapping = {
        'makeup':'Makeup',
        'construction':'Constructi',
        'path':'LineString',
    }
    shape = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/barrier.shp'))
    lm = LayerMapping(Barrier,shape,mapping,
                    transform=False)
    lm.save(strict=True,verbose=True)
    
def checkpoints():
    #Performs layermapping on checkpoints shapefile from PeaceNow
    mapping = {
        'name':'Lable_eng', #misspelled in shapefile
        'checkpoint_type':'TYPE',
        'direction':'btslm_inou',
        'coords':'Point',
    }
    shape = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/checkpoints.shp'))
    lm = LayerMapping(Checkpoint,shape,mapping,
                    transform=False)
    lm.save(strict=True,verbose=True)

def greenline():
    #Performs layermapping on greenline shapefile from PeaceNow
    mapping = {
        'path':'LineString',
    }
    shape = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/green_line.shp'))
    lm = LayerMapping(Border,shape,mapping,
                    transform=False)
    lm.save(strict=True,verbose=True)
    
