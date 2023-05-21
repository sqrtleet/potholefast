from fastapi import FastAPI
from starlette.responses import JSONResponse
from src.mongo import col_potholes
from bson import ObjectId

app = FastAPI()


async def info(_id):
    result = col_potholes.find_one({"_id": ObjectId(_id)}, {"img_detect": 1, "potholes_count": 1})
    img = result["img_detect"]
    count = result["potholes_count"]

    return JSONResponse({"img": img, "potholes_count": count})
