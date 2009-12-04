//DECONFLICT JQUERY AND OPENLAYERS
$j = jQuery.noConflict();

var sphericalMercator = new OpenLayers.Projection("EPSG:900913");
var gps = new OpenLayers.Projection("EPSG:4326");
Proj4js.defs["EPSG:2039"] = '+proj=tmerc +lat_0=31.73439361111111 +lon_0=35.20451694444445 +k=1.0000067 +x_0=219529.584 +y_0=626907.39 +ellps=GRS80 +towgs84=-48,55,52,0,0,0,0 +units=m +no_defs';
var israeltm = new OpenLayers.Projection("EPSG:2039");

var map,popupSelectControl,selectedFeature;

function initMap(){
    map = new OpenLayers.Map({'div':'map',
                  projection: sphericalMercator,
                  displayProjection: israeltm,
                  units: 'm',
                  numZoomLevels: 18,
                  maxResolution: 156543.0339,
                  maxExtent: new OpenLayers.Bounds(-20037508, -20037508, 20037508, 20037508.34)});
    var layer_switcher = new OpenLayers.Control.customLayerSwitcher({'div':OpenLayers.Util.getElement('layerswitcher'),activeColor:'white'});
    map.addControl(layer_switcher);
    
    var cloudmade = new OpenLayers.Layer.CloudMade("OpenStreetMap", {
            projection:sphericalMercator,
            key: '37409ea4915a5145b85ba77588e4cea0',
            styleId: 1551, //farn 1 style, very clean
            infoLink:'/osm/info'});
    map.addLayer(cloudmade);

    //the json parser, defines projections to do transform automatically on load
    //but doesn't actually work
    json_format = new OpenLayers.Format.GeoJSON({
        internalProjection:sphericalMercator,
        externalProjection:israeltm
    });
    
    var border = new OpenLayers.Layer.Vector("Green Line", {
                                                   strategies: [new OpenLayers.Strategy.Fixed()],
                                                   protocol: new OpenLayers.Protocol.HTTP({
                                                       api:"/border",
                                                       url: "/border/json",
                                                       format: json_format}),
                                                   projection:israeltm,
                                                   styleMap:greenlineStyleMap,
                                                   visibility:true,
                                                   infoLink:'/border/info'});
    map.addLayer(border);
    
    settlements = new OpenLayers.Layer.Vector("Settlements", {
                                                strategies: [new OpenLayers.Strategy.Fixed()],
                                                protocol: new OpenLayers.Protocol.HTTP({
                                                    api: "/settlement",
                                                    url: "/settlement/json",
                                                    format: json_format}),
                                                projection:israeltm,
                                                styleMap:settlementStyleMap,
                                                visibility:true,
                                                infoLink:'/settlement/info'});
    map.addLayer(settlements);

    var checkpoints = new OpenLayers.Layer.Vector("Checkpoints", {
                                                   strategies: [new OpenLayers.Strategy.Fixed()],
                                                   protocol: new OpenLayers.Protocol.HTTP({
                                                       api:"/checkpoint",
                                                       url: "/checkpoint/json",
                                                       format: json_format}),
                                                   projection:israeltm,
                                                   styleMap:checkpointStyleMap,
                                                   visibility:false,
                                                   infoLink:'/checkpoint/info'});
    map.addLayer(checkpoints);
    
    var barrier = new OpenLayers.Layer.Vector("Barrier", {
                                                   strategies: [new OpenLayers.Strategy.Fixed()],
                                                   protocol: new OpenLayers.Protocol.HTTP({
                                                       api:"/barrier",
                                                       url: "/barrier/json",
                                                       format: json_format}),
                                                   projection:israeltm,
                                                   styleMap:barrierStyleMap,
                                                   visibility:true,
                                                   infoLink:'/barrier/info'});
    map.addLayer(barrier);

    toolTips = new OpenLayers.Control.ToolTips({bgColor:"white",textColor :"black", bold : true, opacity : 0.75,
	widthValue:"100px"});
	map.addControl(toolTips);

/*	//rollover controller, hover events only
	toolTipSelectControl = new OpenLayers.Control.SelectFeature([settlements,checkpoints,barrier],
        {onSelect: toolTipShow,
        onUnselect: toolTipHide,
        hover:true
        });
    map.addControl(toolTipSelectControl);
	toolTipSelectControl.activate();
*/	
	//popup controller, click events only
    popupSelectControl = new OpenLayers.Control.SelectFeature([settlements,checkpoints,barrier],
        {onSelect: onFeatureSelect,
        onUnselect: onFeatureUnselect,
        hover:false});
	map.addControl(popupSelectControl);
	popupSelectControl.activate();
    //fix selector root container projection
    map.getLayersByClass("OpenLayers.Layer.Vector.RootContainer")[0].projection = israeltm;

    map.setCenter(new OpenLayers.LonLat(3880000, 3755000), 9);
}

/*function onJSONLoad(layer,request) {
    //geojson loader for the vector layers
    var geojson_format = new OpenLayers.Format.GeoJSON();
    var parsed_features = geojson_format.read(request.responseText);
    tmp = parsed_features;
    //have to do reprojection here, because addFeatures doesn't do it
    //probably not mem efficient to do it in JS, should it be serverside?
    for (var i = 0; i < parsed_features.length; i++) {
        var geometry = parsed_features[i].geometry.clone();
        geometry.transform(layer.projection, sphericalMercator);
        layer.addFeatures(geometry);
    }
    layer.addFeatures(parsed_features);
}*/

//POPUP SELECT CALLBACKS
function onPopupClose(evt) {
    popupSelectControl.unselect(selectedFeature);
}
function onFeatureSelect(feature) {
    selectedFeature = feature;
    popup = new OpenLayers.Popup("popup", 
                feature.geometry.getBounds().getCenterLonLat(),
                new OpenLayers.Size(200,100),
                "loading...", true, onPopupClose);
    //create the popup now with blank text
    popup.panMapIfOutOfView = true;
    popup.keepInMap = true;
    popup.setBorder('1px solid black');
    feature.popup = popup;
    OpenLayers.loadURL(feature.layer.protocol.api+"/"+feature.attributes.id+'/popup/',
        {}, null, function(request) {
            selectedFeature.popup.setContentHTML(request.responseText);
            //fill in with the ajax response
    }, null);
    map.addPopup(popup);
    //and show it only when complete
}
function onFeatureUnselect(feature) {
    map.removePopup(feature.popup);
    feature.popup.destroy();
    feature.popup = null;
}

function toolTipShow(feature) {
	var displayText = '';
	displayText += feature.attributes.name;
	toolTips.show({html:displayText});
}
function toolTipHide(feature){
	toolTips.hide();
}


function showSearchMarkers(responseText) {
    response = eval('('+responseText+')');
    
    //our bounds come back in spherical mercator, no need to transform
    var bounds = new OpenLayers.Bounds(response.bounds[0],response.bounds[1],
                                       response.bounds[2],response.bounds[3]);
    //bounds is too tight, need to extend some
    //map.zoomToExtent(bounds);
    

    //markers come back in spherical mercator
    var markers = new OpenLayers.Layer.Markers("Search: "+response.query);
    map.addLayer(markers);
    for (var i = 0; i < response.features.length; i++) {
        var coords = response.features[i].properties.center.coordinates,
            lonlat = new OpenLayers.LonLat(coords[0], coords[1]);
        var marker = new OpenLayers.Marker(lonlat);
        markers.addMarker(new OpenLayers.Marker(lonlat));
    }
}

//JQUERY ONCE PAGE LOADED
$j(document).ready(function() {
    initMap();
    
    //show and hide the layer panel
    $j('a#toggle').click(function() {
        $j(this).next().toggle('fast');
        return false;
      });
      
    //get search input and send to callback
    $j("button[type=submit]#searchButton").click(function(){
        var query = $j("input[type=text]#searchField").val();
        if (query==$j(".defaultText")[0].title) {
            //still default text, do nothing
            //FIXME: this won't work if there's more than one of this class on the page
            return false;
        } else {
            $j.ajax({url:'/settlement/search/'+query,
                    success:showSearchMarkers});
        }
    });
    
    //search input box focus handler
    $j(".defaultText").focus(function(srcc)
    {
        if ($j(this).val() == $j(this)[0].title)
        {
            $j(this).removeClass("defaultTextActive");
            $j(this).val("");
        }
    });
    $j(".defaultText").blur(function()
    {
        if ($j(this).val() == "")
        {
            $j(this).addClass("defaultTextActive");
            $j(this).val($j(this)[0].title);
        }
    });
    $j(".defaultText").blur();
    
    //enable jquery tooltip for infolinks in layerswitcher
    //$j(".layerinfolink").;
});