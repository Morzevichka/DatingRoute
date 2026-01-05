from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import os
import requests


load_dotenv()
app = FastAPI()
GEOSUGGEST_KEY = os.getenv("GEOSUGGEST_KEY")
GEOCODER_KEY = os.getenv("GEOCODER_KEY")
YANDEX_MAPS_API_KEY = os.getenv("YANDEX_MAPS_API_KEY")
YANDEX_GEOCODE_URL = "https://geocode-maps.yandex.ru/v1/"
YANDEX_SUGGEST_URL = "https://suggest-maps.yandex.ru/v1/suggest"

class GeoCodeRequest(BaseModel):
    name: str
    address: str

class GeoCodeResponse(BaseModel):
    name: str
    address: str
    coords: List[float] # [lat, lon]

class GeoGuessRequest(BaseModel):
    name: str
    
class GeoGuessResponse(BaseModel):
    name: str
    address: str

if not GEOSUGGEST_KEY or not GEOCODER_KEY:
    print("⚠ WARNING: KEYS not set in .env")

@app.post(path="/api/maps/coords", response_model=GeoCodeResponse)
def get_coords(payload: GeoCodeRequest):
    query = payload.address

    params = {
        "apikey": GEOCODER_KEY,
        "geocode": query,
        "format": "json"
    }

    response = requests.get(YANDEX_GEOCODE_URL, params=params)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Geocoder unavailable")

    data = response.json()

    try:
        feature = data["response"]["GeoObjectCollection"]["featureMember"][0]
        geo_object = feature["GeoObject"]

        pos = geo_object["Point"]["pos"]
        lon, lat = map(float, pos.split())

        formatted_address = geo_object["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"]

        return GeoCodeResponse(
            name=payload.name,
            address=formatted_address,
            coords=[lat, lon]
        )

    except (KeyError, IndexError, ValueError):
        raise HTTPException(status_code=404, detail="Coordinates not found")

@app.post(path="/api/maps/addresses", response_model=GeoGuessResponse)
def get_addresss(payload: GeoGuessRequest):
    params = {
        "apikey": GEOSUGGEST_KEY,
        "text": payload.name.replace(" ", "+"),
        "lang": "ru_RU",
        "results": 1
    }

    response = requests.get(YANDEX_SUGGEST_URL, params=params)

    print(response.url)
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Suggest service unavailable")

    data = response.json()

    print(data)

    try:
        result = data["results"][0]
        address = result.get("address", {}).get("formatted_address")
        
        if not address:
            address = result.get("subtitle", {}).get("text")
        
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        
        return GeoGuessResponse(
            name=payload.name,
            address=address
        )

    except (KeyError, IndexError, TypeError):
        raise HTTPException(status_code=404, detail="Address not found")

@app.get("/api/maps-key")
def get_key():
    return {"key": YANDEX_MAPS_API_KEY}

@app.get("/api/health")
def health():
    return {"status": "ok"}