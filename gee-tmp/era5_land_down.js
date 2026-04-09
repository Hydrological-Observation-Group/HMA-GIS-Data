//////////////////////////////////////////////////////////////
// Author: xin luo
// Create: 2024.12.9
// Description: download era5 climate data. 
//////////////////////////////////////////////////////////////


var region = ee.Geometry.Rectangle([65, 24, 107, 48], 'EPSG:4326', false);
var year = '2000'

var dset = ee.ImageCollection('ECMWF/ERA5_LAND/MONTHLY_AGGR')
                .filter(ee.Filter.date(year+'-01-01', year+'-12-31'));
print(dset)
/// tempreture
var imgcol_t2m = dset.select(['temperature_2m'])
var t2m_yearly_mean = imgcol_t2m.mean().clip(region).subtract(273.15); // This computes the mean across the collection
print(t2m_yearly_mean)
/// precipitation
var imgcol_tp = dset.select(['total_precipitation_sum'])
var tp_yearly_sum = imgcol_tp.sum().clip(region).multiply(1000); // This computes the sum across the collection
print('11', imgcol_tp)
print(tp_yearly_sum)
/// evaporation
var imgcol_te = dset.select(['total_evaporation_sum'])
var te_yearly_sum = imgcol_te.sum().clip(region).multiply(1000); // This computes the sum across the collection
print(te_yearly_sum)

var visual = {
  // bands: t2p,
  min: 0.0,
  max: 6000,
  palette: [
    '000080', '0000d9', '4000ff', '8000ff', '0080ff', '00ffff',
    '00ff80', '80ff00', 'daff00', 'ffff00', 'fff500', 'ffda00',
    'ffb000', 'ffa400', 'ff4f00', 'ff2500', 'ff0a00', 'ff00ff',
  ]
  };

var empty = ee.Image().byte();
//// outline visualization of the study area.
var scene_outline = empty.paint({
    featureCollection: region, color: 1, width: 3});

Map.centerObject(region, 4);

// Map.addLayer(t2m_yearly_mean, visual, 'total tempreture');
Map.addLayer(tp_yearly_sum, visual, 'total precipitation');
// Map.addLayer(te_yearly_sum, visual, 'total evaporation');
Map.addLayer(scene_outline, {palette: 'FF0000'}, 'training region');

// // Downloading
// var projection = dset.first().projection().getInfo();
// print(projection)
// Export.image.toDrive({
//     image: te_yearly_sum,
//     description: 'era5_land_yearly_te_'+year,
//     folder: 'tmp',
//     scale: 11132,    /// obtained from the document.
//     crs: projection.crs,
//     crsTransform: projection.transform,
//     fileFormat: 'GeoTIFF',
//     region: region
//     });


