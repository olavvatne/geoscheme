# Geoscheme
GeoJson based on United Nations Geoscheme. The regions and subregions include land area and EEZ zone.

![Preview](/docs/geojson-preview.png)

## Recipe - Create Regions
* In QGIS open **Filter** for layer **EZ_Land_v3_202030**
* Filter layer by `UN_TER1`. Get list of M49 codes for region from json file found at **data/json**, or use the curated snippets below
* Save filtered layer to new `GeoJson` layer with data duplication: `Layer | Save As...` 
* Select everything in new layer, and first merge `Edit | Edit Geometry | Merge Selected Features...`, optionally `Vector | Geospatial tools | Buffer` with Selected features only and Dissolve results checked, segments to 1 and distance to 0 and apply, then simplify `Edit | Edit Geometry | Simplify...` (Select tool and click polygon). Use **Simplify by area** with tolerance of **0.5** (**0.15** for less jagged results)
* When using tolerances of 0.5, buffer the perimeter by distance of 0.05 and 1 segment.
* Remove properties from merged GeoJson objects

## Curated Queries
Filter expression that filter vector layer in QGIS to represent Geoscheme's regions and subregions.

[See QUERIES](./QUERIES.md)

## Recipe - Convex Hull of Regions
Create convex hulls that are derived from regions:
```
npm run convex "/data/geojson/africa-hr.geojson"
```

## License
Data → [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
Scripts → [MIT](https://opensource.org/license/mit/)

## Attributions
[Borders provided by Bjørn Sandvik, thematicmapping.org](https://thematicmapping.org/downloads/world_borders.php)

[Flanders Marine Institute (2020). Union of the ESRI Country shapefile and the Exclusive Economic Zones (version 3)](https://www.marineregions.org/downloads.php)