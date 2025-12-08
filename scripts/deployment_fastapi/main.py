from fastapi import FastAPI, UploadFile, HTTPException, File
from typing import Annotated
from PIL import Image
import io
from os import environ as env
import keras

app = FastAPI()


@app.get("/")
async def index():
    model = keras.models.load_model("model/asl_model.keras")
    stringlist = []
    model.summary(print_fn=lambda x: stringlist.append(x))
    return {"details": stringlist}

@app.post("/uploadfile/")
async def create_upload_file(file: Annotated[UploadFile, File()]):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")
    
    image_bytes = await file.read()
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
        width, height = image.size
        image_format = image.format
        
        image.close()

        dummy_result = {
        "image_data": 
            {
                "filename": file.filename,
                "format": image_format,
                "width": width,
                "height": height,
                "size_bytes": len(image_bytes)
            },

        "prediction": 
            {
                'A': 4.2108337650059724e-11,
                'B': 8.935886752770017e-11,
                'C': 0.9999755620956421,
                'D': 3.592570152477492e-08,
                'E': 1.6810101921560516e-10,
                'F': 4.944898179815027e-08,
                'G': 3.058623077034639e-10,
                'H': 1.0961317187252462e-08,
                'I': 2.840615520582901e-10,
                'J': 8.128453964605098e-13,
                'K': 7.140678158360295e-14,
                'L': 1.0155627033769932e-10,
                'M': 4.907019072759172e-14,
                'N': 1.069413741588976e-11,
                'O': 6.209757597019916e-09,
                'P': 1.3683543897968775e-07,
                'Q': 2.3617421902599744e-05,
                'R': 6.767477637309449e-12,
                'S': 5.64855020396271e-13,
                'T': 1.7329658541509474e-10,
                'U': 7.476433209509248e-14,
                'V': 4.321670625528906e-12,
                'W': 9.520202334800665e-12,
                'X': 5.5835978202134484e-12,
                'Y': 1.429532490646035e-12,
                'Z': 1.511469349679828e-08,
                'del': 6.396418825715955e-07,
                'nothing': 1.4256673619428284e-10,
                'space': 3.265508141669926e-10
            }
        }

        return dummy_result


    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not process image: {str(e)}")
    