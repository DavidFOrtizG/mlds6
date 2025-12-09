from fastapi import FastAPI, UploadFile, HTTPException, File
from typing import Annotated
from PIL import Image
import io
from os import environ as env
import keras
from model.prediction import prediction_with_classes
import numpy as np

app = FastAPI()


@app.get("/")
async def index():
    return "Send your image to /uploadfile"

@app.post("/uploadfile/")
async def create_upload_file(file: Annotated[UploadFile, File()]):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")
    
    image_bytes = await file.read()
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        width, height = image.size
        image_format = image.format

        result = {
        "image_data": 
            {
                "filename": file.filename,
                "format": image_format,
                "width": width,
                "height": height,
                "size_bytes": len(image_bytes)
            },

        "prediction": prediction_with_classes(np.array(image), "model/asl_model.keras")
        }

        image.close()

        return result


    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not process image: {str(e)}")
    