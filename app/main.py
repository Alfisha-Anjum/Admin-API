from fastapi import FastAPI
from app.routes import user 
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, HTTPException
from cloudinary import uploader as cloudinary_uploader
import cloudinary

app = FastAPI()



# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, PUT, DELETE, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)

cloudinary.config(
    cloud_name="dsa1ozz2h",
    api_key="435665925159651",
    api_secret="r6HUh4k2wD3ldPhmXx7TcPFQnas"
)

app.include_router(user.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}




@app.post("/upload/", tags=["cloudinary"])
async def upload_image(file: UploadFile = File(...)):
    try:
        result = cloudinary_uploader.upload(
            file.file,
            folder="alfisha/upload-img"
        )
        logo_url = result.get("secure_url")

        if not logo_url:
            raise HTTPException(status_code=500, detail="Failed to upload image")

        return {"url": logo_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))