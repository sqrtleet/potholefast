import os
import uuid
import base64
import shutil
import time

from datetime import datetime
from fastapi import FastAPI, UploadFile
from starlette.responses import JSONResponse

from model.yolo import model
from src.mongo import col_potholes

# Warmup
model.predict("1.png", save=False, imgsz=1280)

app = FastAPI()


@app.post("/image")
async def image(img: UploadFile, latitude, longitude):
    start_time = time.time()

    # сохраняем изображение
    image_name = uuid.uuid4().hex
    image_path = f"static/images/{image_name}.png"

    with open(image_path, "wb") as f:
        shutil.copyfileobj(img.file, f)

    # делаем предсказание модели и сохраняем в папку runs
    res = model.predict(image_path, save=True, imgsz=1280, hide_labels=True)

    # получаем список ограничивающих рамок
    boxes = res[0].boxes
    potholes_count = len(boxes)
    print(f"Potholes count: {potholes_count}")

    with open(f"runs/detect/predict/{image_name}.png", "rb") as f:
        encoded_img_detect = base64.b64encode(f.read()).decode("utf-8")

    # сохраняем в базу данных
    if potholes_count > 0:
        col_potholes.update_one(
            {
                "img_detect": encoded_img_detect
            },
            {
                "$set": {
                    "img_detect": encoded_img_detect,
                    "geo": [latitude, longitude],
                    "potholes_count": potholes_count,
                    "_created": datetime.now(),
                }
            },
            upsert=True
        )
    os.remove(image_path)
    shutil.rmtree("runs")

    print(f"Execution time: {time.time() - start_time} seconds")

    return JSONResponse({"result": encoded_img_detect, "potholes_count": potholes_count})
