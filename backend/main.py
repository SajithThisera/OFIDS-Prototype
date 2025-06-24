import os
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from services.feature_extraction_service import extract_features_and_labels
from services.model_service import train_and_evaluate
import shutil

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Serve images (feature importance/confusion matrix) statically
app.mount("/outputs", StaticFiles(directory=OUTPUT_DIR), name="outputs")

@app.post("/upload")
async def upload(files: list[UploadFile] = File(...)):
    saved = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        saved.append(file.filename)
    return {"saved": saved}

@app.post("/train")
def train_model():
    features, labels, feature_names = extract_features_and_labels(UPLOAD_DIR)
    metrics = train_and_evaluate(features, labels, feature_names, OUTPUT_DIR)
    return {"train_metrics": metrics}

@app.get("/")
def root():
    return {"msg": "OFIDS Prototype API is up"}
