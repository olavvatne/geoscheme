# Geoscheme
GeoJson based on United Nations Geoscheme. The regions include land area and EEZ zone.

![Preview](/docs/geojson-preview.png)

## Recipe - Create Regions
* In QGIS open **Filter** for layer **EZ_Land_v3_202030**
* Filter layer by `UN_TER1`. Get list of M49 codes for region from json file found at **data/json**, or use the curated snippets below
* Save filtered layer to new `GeoJson` layer with data duplication: `Layer | Save As...` 
* Select everything in new layer, and first merge `Edit | Edit Geometry | Merge Selected Features...`, optionally `Vector | Geospatial tools | Buffer` with Selected features only and Dissolve results checked, segments to 1 and distance to 0 and apply, then simplify `Edit | Edit Geometry | Simplify...` (Select tool and click polygon). Use **Simplify by area** with tolerance of **0.5** (**0.15** for less jagged results)
* When using tolerances of 0.5, buffer the perimeter by distance of 0.05 and 1 segment.
* Remove properties from merged GeoJson objects
## Curated Queries
A combination of `UN_TER1` and some assorted missing `UN_SOV1`. Aligns the two sources with each other.

### Europe
```sql
"MRGID_EEZ" = 8361 OR "MRGID_EEZ" = 8363 OR "MRGID_EEZ" = 8364 OR "UN_TER1" IN (8, 70, 100, 208, 372, 233, 40, 203, 246, 250, 276, 300, 191, 348, 352, 380, 428, 112, 440, 703, 438, 807, 470, 56, 234, 20, 292, 833, 442, 492, 499, 248, 528, 578, 616, 620, 642, 498, 643, 705, 724, 752, 756, 826, 804, 674, 688, 336, 744, 831, 832)
```

### Asia
```sql
"UN_SOV1" = 356 OR "UN_TER1" IN (31, 51, 48, 50, 104, 96, 116, 144, 156, 4, 64, 196, 268, 356, 364, 376, 368, 392, 400, 417, 408, 410, 414, 398, 418, 422, 496, 512, 462, 458, 344, 446, 275, 524, 586, 634, 608, 682, 702, 760, 764, 762, 792, 795, 860, 704, 887, 360, 784, 626, 158)
```

### Americas
```sql
"MRGID_EEZ" = 8495 OR "MRGID_EEZ" = 21803 OR "MRGID_EEZ" = 48952 OR  "MRGID_EEZ" = 62598 OR  "MRGID_EEZ" = 62596 OR  "MRGID_EEZ" = 48984 OR  "MRGID_EEZ" = 48985 OR  "MRGID_EEZ" = 26517 OR  "MRGID_EEZ" = 26518 OR "MRGID_EEZ" = 8463 OR "MRGID_EEZ" = 8463 OR "MRGID_EEZ" = 8453 OR "MRGID_EEZ" = 8452 OR  "MRGID_EEZ" = 8401 OR "UN_SOV1" = 76 OR "UN_SOV1" = 332 OR "UN_SOV1" = 152 OR "UN_SOV1" = 218 OR "UN_TER1" IN (28,32,52,60,44,84,68,76,124,152,136,170,188,192,212,214,218,222,254,238,308,304,320,328,332,340,388,474,500,484,533,660,740,558,600,604,591,630,659,662,780,840,858,670,862,92,850,312,530,666,796,535)
```

### Oceania
```sql
"MRGID_EEZ" = 8451 OR  "MRGID_EEZ" = 8442 OR "MRGID_EEZ" = 8443 OR "MRGID_EEZ" = 8444 OR "MRGID_EEZ" = 48948 OR "MRGID_EEZ" = 8319 OR "UN_TER1" IN (16,36,90,184,242,583,258,316,296,540,570,580,574,548,520,554,598,772,776,798,876,882,612,585,584)
```

### Africa
```sql
"MRGID_EEZ" = 48946 OR "UN_TER1" = 260 OR "UN_TER1" = 654 OR "UN_TER1" = 638 OR "UN_TER1" = 175 OR "UN_SOV1" IN (12,24,204,178,180,108,120,148,174,140,132,262,818,226,232,231,270,266,288,324,384,404,430,434,450,466,504,480,478,508,454,562,175,566,624,638,646,690,710,426,72,686,694,706,736,768,678,788,834,800,854,516,748,894,716,654,732, 728, 729)
```

### Antarctica
```sql
"MRGID_EEZ" = 8489
```

### Subregions
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