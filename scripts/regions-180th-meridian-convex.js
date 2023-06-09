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


function isClockwise(vertices) {
    let sum = 0.0;
    if (vertices.length < 4) {
        throw Error("Must provide a polygon ring");
    }

    for (let i = 0; i < vertices.length; i++) {
        let v1 = vertices[i];
        let v2 = vertices[(i + 1) % vertices.length];
        sum += (v2[0] - v1[0]) * (v2[1] + v1[1]);
    }
    return sum > 0.0;
}


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

let outputName = p.replace("-hr", "");
outputName = outputName.replace(".geojson", "");
outputName = outputName + "-convex.geojson";
// TODO: find a vertical line not occupied automatically
// all -60, except americas +40
const splitLine = -60;
const allBbox = [-179.9,-90, 179.9, 90];
const data = JSON.parse(readFileSync(p));
const clipped = bboxClip(data.features[0], allBbox);

// The bounding boxes are set a bit conservatively. Can go closer to [-180, 180] and [-90, 90]
const leftBbox = [splitLine,-89.5, 179.5, 89.5];
const rightBbox = [-179.5,-89.5, splitLine, 89.5];
const leftClipped = bboxClip(clipped, leftBbox);
const rightClipped = bboxClip(clipped, rightBbox);
const leftResult = convex(leftClipped)
const rightResult = convex(rightClipped)

const mp = [];

if (leftResult) {
    const leftCoords = leftResult.geometry.coordinates;
    if (isClockwise(leftCoords[0])) {
        leftCoords[0] = leftCoords[0].slice().reverse();
    }
    mp.push(leftCoords);
}
if (rightResult) {
    const rightCoords = rightResult.geometry.coordinates;
    if (isClockwise(rightCoords[0])) {
        rightCoords[0] = rightCoords[0].slice().reverse();
    }
    mp.push(rightCoords);
}
    const result = multiPolygon(mp);
writeFileSync(outputName, JSON.stringify(result));