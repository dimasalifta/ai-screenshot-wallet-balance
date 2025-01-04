import google.generativeai as genai
from google.generativeai.types import generation_types
import PIL.Image
import json
import os
# 1. Konfigurasi Pengaturan Generasi
generation_config = generation_types.GenerationConfig(
    temperature=0.7,
    top_p=0.9,
    top_k=50,
    max_output_tokens=1024,
)

# # 2. Instruksi Sistem (Opsional - Menentukan perilaku model)
# system_instruction = genai.Content(
#     role="system",
#     parts=[
#         genai.Part(text="Anda adalah asisten AI yang membantu dalam pengecekan saldo dari input user screenshot wallet/rekening lalu anda hanya mengirim output berupa json yang berisi saldo. ketika ada input user selain gambar, maka jawab 'WRONG INPUT'")
#     ]
# )

# 3. Konfigurasi API
genai.configure(api_key=os.environ["GEMINI_API_KEY"], transport="rest")


# 4. Membuat Model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "Anda adalah asisten AI yang membantu dalam pengecekan saldo dari input user screenshot wallet/rekening lalu anda hanya mengirim output berupa json yang berisi saldo. ketika ada input user selain gambar, maka jawab 'WRONG INPUT'"},
        {"role": "user", "parts": "anda mengirimkan format json sepert ini {'format1': 100000000.00,\n'format2': 'Rp 100.000.000,00',\n'format3': 'seratus juta rupiah'}"},
        # {"role": "user", "parts": "saldo_str jumlah utama saldo menggunakan tanda '.' lalu tanda ',' contoh: 1.000.000,00"},
    ]
)
# 5. Menghasilkan Respons
screenshot_image = PIL.Image.open("ss (1).jpg")

response = chat.send_message(screenshot_image)
# print(response.text)
result = response.text.replace('```json\n', '').replace('\n```', '').strip()
# print(result)
try:
    result_json = json.loads(result)  # Parsing ke JSON
    result_json["id"] = id
except json.JSONDecodeError:  # Jika bukan JSON valid
    result_json = {"error": "Invalid JSON format"}  # Berikan error sebagai respons
    
print(result_json)