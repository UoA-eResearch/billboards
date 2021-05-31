#!/usr/bin/env python3
import json
import googlemaps
import sys
import os
import pandas as pd
from tqdm import tqdm
tqdm.pandas()

gmaps = googlemaps.Client(key=os.environ["GOOGLE_API_KEY"])
print(gmaps)

df = pd.read_excel("misc/May-2021-Licences.xlsx", skiprows=1)
df = df[df.LicenceType == "Off-licence"]

cols = ["Premises Name", "Premises Street", "Premises Suburb", "Premises City"]
df["address"] = df.progress_apply(lambda row: 
    ", ".join([row[k] for k in cols if not pd.isna(row[k])]),
    axis=1
)
df["geo"] = df.address.progress_apply(lambda address: gmaps.geocode(address, components={"country": "NZ"}))
df.to_json("data/ARLA.json", 'records')