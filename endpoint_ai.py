from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import os
from datetime import datetime
import google.generativeai as genai
from google.generativeai.types import generation_types
import PIL.Image
import json

load_dotenv()
# Mengakses variabel lingkungan GEMINI_API_KEY
api_key = os.getenv("GEMINI_API_KEY")
app = FastAPI()

async def generate_response(id: int , image_path: str):
    # 1. Konfigurasi Pengaturan Generasi
    generation_config = generation_types.GenerationConfig(
        temperature=0.7,
        top_p=0.9,
        top_k=50,
        max_output_tokens=1024,
    )

    # 3. Konfigurasi API
    genai.configure(api_key=api_key, transport="rest")

    # 4. Membuat Model
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": "Anda adalah asisten AI yang membantu dalam pengecekan saldo dari input user screenshot wallet/rekening lalu anda hanya mengirim output berupa json yang berisi saldo. ketika ada input user selain gambar, maka jawab 'WRONG INPUT'"},
            {"role": "user", "parts": 'anda mengirimkan format json sepert ini {"format1": 100000000.00,"format2": "Rp 100.000.000,00","format3": "seratus juta rupiah"}'},
            # {"role": "user", "parts": "saldo_str jumlah utama saldo menggunakan tanda '.' lalu tanda ',' contoh: 1.000.000,00"},
        ]
    )
    # 5. Menghasilkan Respons
    screenshot_image = PIL.Image.open(image_path)

    response = chat.send_message(screenshot_image)
    # print(response.text)
    result = response.text.replace('```json\n', '').replace('\n```', '').strip()
    # print(result)
    try:
        result_json = json.loads(result)  # Parsing ke JSON
        result_json["id"] = id
    except json.JSONDecodeError:  # Jika bukan JSON valid
        result_json = {"error": "Invalid JSON format"}  # Berikan error sebagai respons

    return result_json

@app.post("/upload-image/{id}")
async def upload_image(id: str, file: UploadFile = File(...)):
    try:
        # Membaca gambar yang di-upload
        image_bytes = await file.read()
        image = Image.open(BytesIO(image_bytes))

        # Menambahkan timestamp saat penerimaan gambar
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Format timestamp: YYYYMMDDHHMMSS

        # Menentukan nama file berdasarkan ID dan timestamp
        file_name = f"{id}_{timestamp}.png"  # Menggunakan ID dan timestamp untuk nama file

        # Menyimpan gambar dengan nama sesuai ID dan timestamp
        os.makedirs("uploads", exist_ok=True)  # Membuat folder uploads jika belum ada
        image.save(os.path.join("uploads", file_name))

        # Menghasilkan respons dari gambar yang di-upload
        response = await generate_response(id,os.path.join("uploads", file_name))
        return JSONResponse(content=response, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": f"Error: {str(e)}"}, status_code=500)

# Untuk menjalankan server
# uvicorn main:app --reload
