# QGIS Subregion Queries
Filter `TM_WORLD_BORDERS_SIMPL-0.3` map by SUBREGION and then export layer as a `XLSX` to extract M49 codes. `=TEXTJOIN(",";TRUE;D2:D1000)` in Excel to join M49 codes together.

## Europe
### Southern Europe
```sql
"MRGID_EEZ" = 8361 OR "MRGID_EEZ" = 8363 OR "MRGID_EEZ" = 8364 OR "UN_TER1" IN (8,20,70,191,292,300,336,380,470,499,620,674,688,705,724,807)
```

### Northern Europe
```sql
"UN_TER1" IN (208,372,233,246,352,428,440,234,833,248,578,752,826,744,831,832)
```

### Western Europe
```sql
"UN_TER1" IN (40,250,276,438,56,442,492,528,756)
```

### Eastern Europe
```sql
"UN_TER1" IN (100,203,348,112,703,616,642,498,643,804)
```

## Americas
### Northern America
```sql
"MRGID_EEZ" = 8402 OR "MRGID_EEZ" = 8452 OR  "MRGID_EEZ" = 8453 OR "MRGID_EEZ" = 8463 OR "UN_TER1" IN (60,124,304,840,666)
```

### Latin America and the Caribbean
```sql
"MRGID_EEZ" = 21787 OR "MRGID_EEZ" = 8403 OR "UN_TER1" IN (28,32,52,44,84,68,76,152,136,170,188,192,212,214,218,222,254,238,308,320,328,332,340,388,474,500,484,533,660,740,558,600,604,591,630,659,662,780,858,670,862,92,850,312,530,796,663,652)
```

## Asia
### Eastern Asia
```sql
"UN_TER1" IN (156,392,408,410,496,344,446)
```

### Southern Asia
```sql
"MRGID_EEZ" = 8333 OR "UN_TER1" IN (50,144,4,64,356,364,462,524,586)
```

### South-eastern Asia
```sql
"UN_TER1" IN (104,96,116,418,458,608,702,764,704,360,626)
```

### Central Asia
```sql
"UN_TER1" IN (417,398,762,795,860)
```

### Western Asia
```sql
"UN_TER1" IN (31,51,48,196,268,376,368,400,414,422,512,275,634,682,760,792,887,784)
```

## Africa
### Northern Africa
```sql
"UN_TER1" IN (12,818,434,504,736,788,732,729)
```

### Sub-Saharan Africa
```sql
"MRGID_EEZ" = 22598 OR "UN_TER1" IN (24,204,178,180,108,120,148,174,140,132,262,226,232,231,270,266,288,324,384,404,430,450,466,480,478,508,454,562,175,566,624,638,646,690,710,426,72,686,694,706,768,678,834,800,854,516,748,894,716,654,728)
```

## Oceania
### Australia and New Zealand
```sql
"UN_TER1" IN (36,574,554,162,166,334)
```

### Melanesia
```sql
"UN_TER1" IN (90,242,540,548,598)
```

### Micronesia
```sql
"UN_TER1" IN (583,316,296,580,520,585,584,581)
```

### Polynesia
```sql
"UN_TER1" IN (16,184,258,570,772,776,798,876,882,612)
```