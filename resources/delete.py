from fastapi import FastAPI
from starlette.responses import JSONResponse
from src.mongo import col_potholes
from bson import ObjectId
from pymongo.results import DeleteResult

app = FastAPI()


async def delete(_id):
    result: DeleteResult = col_potholes.delete_one({"_id": ObjectId(_id)})

    if result.deleted_count == 1:
        return JSONResponse({"message": "Record deleted successfully"})
    else:
        return JSONResponse({"error": "Record not found"}, status_code=404)
