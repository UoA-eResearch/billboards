#!/usr/bin/env python3
import json
import requests
import sys
import os
import pandas as pd
pd.set_option('display.max_columns', None)
from tqdm import tqdm
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

tqdm.pandas()
df = pd.read_excel("February-2025-Licences.xlsx", skiprows=1)

cols = ["Premises Name", "Premises Street", "Premises Suburb", "Premises City"]
df["address"] = df.apply(lambda row: 
    ", ".join([row[k] for k in cols if not pd.isna(row[k])]),
    axis=1
)
print(df.address)
def geocode(address):
    try:
        r = requests.post('https://places.googleapis.com/v1/places:searchText', json={
                "textQuery" : address,
                "pageSize": 1,
                "locationRestriction": {
                    "rectangle": {
                        #158.185443,-52.720720,187.811214,-30.693290
                        "low": {
                            "latitude": -52.720720,
                            "longitude": 158.185443
                        },
                        "high": {
                            "latitude": -30.693290,
                            "longitude": 180
                        }
                    }
                }
            }, headers={
                'X-Goog-Api-Key': os.environ["GOOGLE_API_KEY"],
                'X-Goog-FieldMask': 'places.location,places.displayName,places.formattedAddress,places.servesBeer,places.servesWine'
        })
        return r.json()["places"][0]
    except Exception as e:
        print(e)
        return None

results = pd.json_normalize(df.address.progress_apply(geocode))
print(results)
results.to_csv("data/ARLA.csv")