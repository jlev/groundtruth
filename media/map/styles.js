var settlementStyleMap = new OpenLayers.StyleMap({
  fillOpacity:0.4,
  fillColor:'#000066',
  stroke:'true',
  strokeColor:'#0000FF'
});

var barrierStyleMap = new OpenLayers.StyleMap({
  strokeWidth:3,
  strokeColor:'#FF0000'
});
var barrierStyleLookup = {
  "Completed": {strokeDashstyle: 'solid', strokeColor:'#FF0000'},
  "Road Protection": {strokeDashstyle: 'solid', strokeColor:'#FF0000'},
  "Under Construction": {strokeDashstyle: 'longdash', strokeColor:'#FF0000'},
  "Built and Cancelled": {strokeDashstyle: 'dash', strokeColor:'#000000'},
  "Planned": {strokeDashstyle: 'dash', strokeColor:'#7F43B6'},
  "Subject to Further Inter-Ministerial Examination": {strokeDashstyle: 'dot', strokeColor:'#7F43B6'}
};
barrierStyleMap.addUniqueValueRules("default", "construction", barrierStyleLookup);
barrierStyleMap.addUniqueValueRules("select", "construction", barrierStyleLookup);

var checkpointStyleMap = new OpenLayers.StyleMap(
  {pointRadius: 10,
  fillOpacity:1,
  externalGraphic:"/media/map/icons/checkpoint.gif",
  strokeColor:'#FF0000'});
var checkpointStyleLookup = {
  "Checkpoint": {externalGraphic:"/media/map/icons/checkpoint.gif"},
  "Earth Mound": {externalGraphic:"/media/map/icons/checkpoint.gif"},
  "Observation Tower": {externalGraphic:"/media/map/icons/tower.gif"},
  "DCO": {externalGraphic:"/media/map/icons/dco.png"},
  "Partial Checkpoint": {externalGraphic:"/media/map/icons/checkpoint.gif"},
  "Road Block": {externalGraphic:"/media/map/icons/checkpoint.gif"},
  "Road Gate": {externalGraphic:"/media/map/icons/checkpoint.gif"},
  "Agricultural Gate": {externalGraphic:"/media/map/icons/checkpoint.gif"}
};
checkpointStyleMap.addUniqueValueRules("default", "type", checkpointStyleLookup);
checkpointStyleMap.addUniqueValueRules("select", "type", checkpointStyleLookup);

var greenlineStyleMap = new OpenLayers.StyleMap({
  strokeWidth:3,
  strokeColor:'#006600'
});

var osloAStyleMap = new OpenLayers.StyleMap({
  fillOpacity:0.5,
  fillColor:'#B79E80',
  strokeWidth:2,
  strokeColor:'#B79E80'
});

var osloBStyleMap = new OpenLayers.StyleMap({
  fillOpacity:0.5,
  fillColor:'#E2D1AC',
  strokeWidth:2,
  strokeColor:'#E2D1AC'
});
    
var osloCStyleMap = new OpenLayers.StyleMap({
  fillOpacity:0.5,
  fillColor:'#F2E6C8',
  strokeWidth:1,
  strokeColor:'#F2E6C8'
});