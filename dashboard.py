from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from io import BytesIO
import requests
from PIL import Image
from fastapi import Request

# Inisialisasi FastAPI dan Jinja2 Templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# URL API untuk mengirim gambar
FASTAPI_URL = "http://localhost:8001/upload-image/"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "user_id": "123", "result": None})

@app.post("/upload-image/{user_id}", response_class=HTMLResponse)
async def upload_image(request: Request, user_id: str, file: UploadFile = File(...)):
    try:
        # Membaca gambar yang di-upload
        image_bytes = await file.read()
        image = Image.open(BytesIO(image_bytes))

        # Mengirim gambar ke FastAPI endpoint untuk pemeriksaan saldo
        files = {"file": image_bytes}
        response = requests.post(f"{FASTAPI_URL}{user_id}", files=files)

        # Menampilkan hasil respons JSON dari API
        if response.status_code == 200:
            result = response.json()
            return templates.TemplateResponse("index.html", {"request": request, "user_id": user_id, "result": result})
        else:
            return templates.TemplateResponse("index.html", {"request": request, "user_id": user_id, "result": {"error": "Error from API"}})
    
    except Exception as e:
        return templates.TemplateResponse("index.html", {"request": request, "user_id": user_id, "result": {"error": str(e)}})

# Menjalankan server dengan uvicorn
# uvicorn dashboard:app --reload --host 0.0.0.0 --port 8000
