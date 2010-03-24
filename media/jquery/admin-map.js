//DECONFLICT JQUERY AND OPENLAYERS
$j = jQuery.noConflict();

//globals to store
var center,zoom;

$j(document).ready(function() {
  function linkMaps(e) {
    var map = e.object;
    center = map.center.clone();
    zoom = map.zoom;
    console.log(center.lat+","+center.lon+"@"+zoom);
    
    OpenLayers.Event.stop(e);
    for(var i=1; i < olwidget.maps.length; i++) {
      olwidget.maps[i].moveTo(center, zoom, {
          'dragging': false, //don't issue in-between events
          'noEvent': true //don't issue end events either
      });
    }
  }

  //for(var i=0; i < olwidget.maps.length; i++) {
  //make the first map the master, because otherwise we get inf loops
    map = olwidget.maps[0];
    map.events.register('move', this, linkMaps);
  //}
});
