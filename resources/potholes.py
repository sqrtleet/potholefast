from fastapi import FastAPI
from starlette.responses import JSONResponse
from src.mongo import col_potholes

app = FastAPI()


@app.get("/potholes")
async def potholes():
    results = list(col_potholes.find({}, {"geo": 1, "_id": 1}))
    geo_data = []

    for result in results:
        latitude = result["geo"][0]
        longitude = result["geo"][1]
        obj_id = str(result["_id"])
        geo_data.append({"id": obj_id, "latitude": latitude, "longitude": longitude})

    return JSONResponse(geo_data)
