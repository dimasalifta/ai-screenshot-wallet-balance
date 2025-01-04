# ai-screenshot-wallet-balance

Proyek ini memungkinkan pengguna untuk mengunggah gambar screenshot dan menerima informasi saldo berupa JSON yang dapat digunakan untuk pengecekan saldo dari rekening atau wallet berdasarkan gambar yang diunggah.

## Contoh Request

### 1. Menggunakan **Postman**

Untuk menguji API menggunakan **Postman**, lakukan langkah-langkah berikut:

- **URL**: `http://localhost:8000/upload-image/{id}`  
  Gantilah `{id}` dengan ID unik yang Anda inginkan untuk request ini (misalnya `1234`).

- **Method**: `POST`

- **Body Type**: `form-data`

- **Key**: `file`
- **Value**: Pilih file gambar dari komputer Anda (misalnya `path/to/image.png`).

**Contoh**:

| Key  | Value             |
| ---- | ----------------- |
| file | path/to/image.png |

> **Catatan**: ID dalam URL adalah ID unik yang digunakan untuk setiap request. Anda dapat menggantinya dengan ID yang sesuai.

### 2. Menggunakan **curl** di Windows CMD

Jika Anda ingin mengirim request menggunakan **curl** di terminal atau CMD (Command Prompt) di Windows, gunakan perintah berikut:

```bash
curl -X POST http://127.0.0.1:8000/upload-image/1234 -F "file=@path/to/image.png"
```
