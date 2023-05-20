import pymongo
import config

server = f"mongodb://{config.MONGO_USERNAME}:{config.MONGO_PASSWORD}@{config.MONGO_HOST}:{config.MONGO_PORT}/"
local = "mongodb://localhost:27017"


client = pymongo.MongoClient(
    local
)

db = client["pothole"]

col_potholes = db["potholes"]