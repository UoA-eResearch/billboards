#!/usr/bin/env python

import pprint
import json

with open("data/ARLA.json", "r") as f:
    data = json.load(f)

features = []
for d in data:
    if d.get("geo"):
        lat = d["geo"][0]["geometry"]["location"]["lat"]
        lng = d["geo"][0]["geometry"]["location"]["lng"]
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lng, lat]
            },
            "properties": d
        })

geojson = {
    "type": "FeatureCollection",
    "features": features
}

with open("data/ARLA.geojson", "w") as f:
    json.dump(geojson, f)

