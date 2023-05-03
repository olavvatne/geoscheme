#!/usr/bin/env node

/*
Convex hull that accounts for 180th meridian. 
Result is a MultiPolygon with one or two convex hull polygons split by the
180th meridian, as recommended by the GeoJson spec:
https://datatracker.ietf.org/doc/html/rfc7946#section-3.1.9
*/

import { argv } from 'node:process';
import {lstatSync, readFileSync, writeFileSync} from 'node:fs';
import {extname} from 'node:path';
import convex from '@turf/convex';
import bboxClip from '@turf/bbox-clip';
import {multiPolygon} from '@turf/helpers';

if (argv.length < 2) {
    throw Error("No valid argv")
}

const args = process.argv.slice(2);
if (args.length != 1) {
    throw Error("Missing path")
}

const p = args[0]
if (!lstatSync(p).isFile() || extname(p) !== ".geojson") {
    throw Error("Not a geojson file")
}
// TODO: find a vertical line not occupied automatically
// all -40, except americas +40
const splitLine = 40;
const allBbox = [-179.9,-90, 179.9, 90];
const data = JSON.parse(readFileSync(p));
const clipped = bboxClip(data.features[0], allBbox);

const leftBbox = [splitLine,-90, 179.9, 90];
const rightBbox = [-179.9,-90, splitLine, 90];
const leftClipped = bboxClip(clipped, leftBbox);
const rightClipped = bboxClip(clipped, rightBbox);
const leftResult = convex(leftClipped)
const rightResult = convex(rightClipped)

const mp = [];

if (leftResult) {
    const leftCoords = leftResult.geometry.coordinates;
    leftCoords[0] = leftCoords[0].slice().reverse();
    mp.push(leftCoords);
}
if (rightResult) {
    const rightCoords = rightResult.geometry.coordinates;
    rightCoords[0] = rightCoords[0].slice().reverse();
    mp.push(rightCoords);
}
    const result = multiPolygon(mp);
writeFileSync('temp-convex.geojson', JSON.stringify(result));