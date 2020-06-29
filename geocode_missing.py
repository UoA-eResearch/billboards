#!/usr/bin/env python3
import json
import googlemaps
import sys
import os

gmaps = googlemaps.Client(key=os.environ["GOOGLE_API_KEY"])
print(gmaps)
filename = sys.argv[1]

with open(filename) as f:
    data = json.load(f)

for d in data:
    if d.get("address") and not d.get("latitude"):
        result = gmaps.geocode(d["address"])
        print(result)
        result = result[0]["geometry"]["location"]
        d["latitude"] = result["lat"]
        d["longitude"] = result["lng"]

with open(filename, "w") as f:
    json.dump(data, f)