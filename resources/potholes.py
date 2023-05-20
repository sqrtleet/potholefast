from fastapi import FastAPI
from starlette.responses import JSONResponse
from src.mongo import col_potholes

app = FastAPI()


@app.get("/potholes")
async def potholes():
    results = list(col_potholes.find({}, {"_id": 1, "img_detect": 1, "geo": 1, "potholes_count": 1}))
    geo_data = []

    for result in results:
        latitude = result["geo"][0]
        longitude = result["geo"][1]
        obj_id = str(result["_id"])
        img = result["img_detect"]
        count = result["potholes_count"]
        geo_data.append(
            {"id": obj_id, "latitude": latitude, "longitude": longitude, "img": img, "potholes_count": count})

    return JSONResponse(geo_data)
