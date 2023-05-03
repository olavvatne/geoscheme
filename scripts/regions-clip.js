#!/usr/bin/env node
import { argv } from 'node:process';
import {lstatSync, readFileSync, writeFileSync} from 'node:fs';
import {extname} from 'node:path';
import bboxClip from '@turf/bbox-clip';

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

const data = JSON.parse(readFileSync(p));
var bbox = [-180, -90, 180, 90];
const result = bboxClip(data.features[0], bbox);
writeFileSync('temp-convex.geojson', JSON.stringify(result));