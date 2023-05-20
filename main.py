import uvicorn
from fastapi import FastAPI, Request, UploadFile, File, Form

from resources.home import home as home_handler
from resources.image import image as image_handler
from resources.realtime import real_time as realtime_handler
from resources.potholes import potholes as potholes_handler

app = FastAPI()


@app.get("/")
async def home(request: Request):
    return await home_handler(request)


@app.post("/image")
async def image(img: UploadFile = File(...), latitude: float = Form(...), longitude: float = Form(...)):
    return await image_handler(img, latitude, longitude)


@app.post("/realtime")
async def realtime(img: UploadFile = File(...), latitude: float = Form(...), longitude: float = Form(...)):
    return await realtime_handler(img, latitude, longitude)


@app.get("/potholes")
async def potholes():
    return await potholes_handler()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7777)
