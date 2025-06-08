# **API Pelacak Investasi**

Proyek ini adalah REST API sederhana yang dibangun dengan Django dan Django REST Framework untuk melacak investasi pengguna. Ini berfungsi sebagai tes penyaringan awal untuk menilai keterampilan dasar pengembangan backend. API ini memungkinkan pengguna yang terautentikasi untuk mengelola investasi mereka, melihat kinerja portofolio, dan mendapatkan wawasan tentang kebiasaan investasi mereka.

## **Struktur Proyek**

investment-tracker/  
├── manage.py  
├── requirements.txt  
├── README.md  
├── config/  
│   ├── \_\_init\_\_.py  
│   ├── asgi.py  
│   ├── settings.py  
│   ├── urls.py  
│   └── wsgi.py  
├── apps/  
│   ├── \_\_init\_\_.py  
│   ├── investments/  
│   │   ├── \_\_init\_\_.py  
│   │   ├── admin.py  
│   │   ├── apps.py  
│   │   ├── migrations/  
│   │   ├── models.py  
│   │   ├── serializers.py  
│   │   ├── services.py  
│   │   ├── urls.py  
│   │   └── views.py  
└── fixtures/  
    └── sample\_data.json

## **Instruksi Pengaturan**

1. **Clone repositori ini:**  
   git clone \<url-repo-anda\>  
   cd investment-tracker

2. **Buat lingkungan virtual dan aktifkan:**  
   python \-m venv venv  
   source venv/bin/activate  \# Di Windows, gunakan \`venv\\Scripts\\activate\`

3. **Instal dependensi yang dibutuhkan:**  
   pip install \-r requirements.txt

4. **Buat migrasi database untuk aplikasi** investments**:**  
   python manage.py makemigrations investments

5. **Terapkan migrasi database untuk membuat tabel:**  
   python manage.py migrate

6. **Muat data sampel (Opsional):**  
   python manage.py loaddata fixtures/sample\_data.json

   Perintah ini akan membuat superuser (admin) dengan kata sandi adminpassword serta beberapa data investasi dan transaksi sampel.  
7. **Jalankan server pengembangan:**  
   python manage.py runserver

   API akan tersedia di http://127.0.0.1:8000/.

## **Endpoint API**

URL dasar untuk API adalah /api/v1/.

### **Autentikasi**

API ini menggunakan JWT untuk autentikasi. Untuk mengakses endpoint yang dilindungi, Anda perlu mendapatkan token dan menyertakannya dalam header Authorization sebagai Bearer token.

* **POST** /api/token/  
  * Dapatkan token JWT dengan memberikan username dan password.  
* **POST** /api/token/refresh/  
  * Perbarui token JWT yang sudah kedaluwarsa menggunakan refresh token.

### **Investasi**

* **GET** /api/v1/investments/  
  * **Deskripsi:** Mengambil daftar investasi (dengan paginasi) untuk pengguna yang terautentikasi, diurutkan berdasarkan tanggal pembelian (terbaru dulu).  
  * **Header:** Authorization: Bearer \<token\_akses\_anda\>  
  * **Respons:**  
    {  
        "count": 2,  
        "next": null,  
        "previous": null,  
        "results": \[  
            {  
                "id": 1,  
                "asset\_name": "Saham Tesla",  
                "amount\_invested": "10000.00",  
                "purchase\_date": "2025-06-01T12:00:00Z",  
                "current\_value": "12000.00",  
                "is\_active": true,  
                "profit\_loss": "2000.00",  
                "profit\_loss\_percentage": "20.00"  
            }  
        \]  
    }

* **POST** /api/v1/investments/  
  * **Deskripsi:** Membuat investasi baru untuk pengguna yang terautentikasi. Log transaksi 'PURCHASE' yang sesuai akan dibuat secara otomatis.  
  * **Header:** Authorization: Bearer \<token\_akses\_anda\>  
  * **Body:**  
    {  
        "asset\_name": "Saham Apple",  
        "amount\_invested": "5000.00",  
        "current\_value": "5100.00",  
        "purchase\_date": "2025-06-08T10:00:00Z"  
    }

  * **Validasi:** amount\_invested harus minimal $1000.  
  * **Respons (201 Created):** Objek investasi yang baru dibuat.  
* **GET** /api/v1/investments/summary/  
  * **Deskripsi:** Memberikan ringkasan data agregat dari portofolio investasi pengguna.  
  * **Header:** Authorization: Bearer \<token\_akses\_anda\>  
  * **Respons:**  
    {  
        "total\_invested": "35000.00",  
        "current\_portfolio\_value": "36000.00",  
        "total\_profit\_loss": "1000.00",  
        "overall\_roi\_percentage": "2.86",  
        "active\_investments\_count": 2,  
        "best\_performing\_investment": { "...data investasi terbaik..." },  
        "worst\_performing\_investment": { "...data investasi terburuk..." },  
        "insights": {  
            "average\_holding\_period\_days": 270.5,  
            "preferred\_investment\_size": 17500.00  
        }  
    }

## **Database**

Proyek ini menggunakan **SQLite** untuk kemudahan pengaturan, sesuai dengan persyaratan tugas. Tidak diperlukan server database eksternal.

## **Contoh Perintah** curl

1. Dapatkan Token:  
   Windows (Command Prompt / PowerShell):  
   curl \-X POST http://127.0.0.1:8000/api/token/ \-H "Content-Type: application/json" \-d "{\\"username\\": \\"admin\\", \\"password\\": \\"katasandibaruanda\\"}"

   **macOS / Linux (Bash / Zsh):**  
   curl \-X POST http://127.0.0.1:8000/api/token/ \-H "Content-Type: application/json" \-d '{"username": "admin", "password": "katasandibaruanda"}'

2. **Lihat Daftar Investasi:**  
   curl \-X GET http://127.0.0.1:8000/api/v1/investments/ \-H "Authorization: Bearer \<token\_akses\_anda\>"

3. Buat Investasi:  
   Windows (Command Prompt / PowerShell):  
   curl \-X POST http://127.0.0.1:8000/api/v1/investments/ \-H "Content-Type: application/json" \-H "Authorization: Bearer \<token\_akses\_anda\>" \-d "{\\"asset\_name\\": \\"Dana Teknologi Baru\\", \\"amount\_invested\\": \\"2500\\", \\"current\_value\\": \\"2500\\", \\"purchase\_date\\": \\"2025-06-08T10:00:00Z\\"}"

   **macOS / Linux (Bash / Zsh):**  
   curl \-X POST http://127.0.0.1:8000/api/v1/investments/ \-H "Content-Type: application/json" \-H "Authorization: Bearer \<token\_akses\_anda\>" \-d '{"asset\_name": "Dana Teknologi Baru", "amount\_invested": "2500", "current\_value": "2500", "purchase\_date": "2025-06-08T10:00:00Z"}'

4. **Dapatkan Ringkasan:**  
   curl \-X GET http://127.0.0.1:8000/api/v1/investments/summary/ \-H "Authorization: Bearer \<token\_akses\_anda\>"

## **Asumsi yang Dibuat**

* current\_value dari sebuah investasi disediakan oleh pengguna saat pembuatan dan dapat diperbarui melalui admin Django atau endpoint PATCH di masa depan (tidak termasuk dalam tes ini).  
* Flag is\_active secara default adalah True untuk investasi baru.  
* Perhitungan laba/rugi didasarkan pada rumus sederhana: current\_value \- amount\_invested.  
* reference\_id untuk transaksi adalah UUID unik yang dibuat secara otomatis saat pembuatan.

## **Penyelesaian Masalah (Troubleshooting)**

### **Galat "No active account found with the given credentials"**

Jika Anda mendapatkan galat ini saat mencoba mendapatkan token, ini berarti kata sandi yang Anda berikan tidak cocok dengan yang ada di database. Anda dapat mengatur ulang kata sandi untuk pengguna admin dengan menjalankan perintah berikut dan mengikuti petunjuknya:

python manage.py changepassword admin

Setelah Anda mengatur kata sandi baru, gunakan kata sandi tersebut dalam perintah curl untuk mendapatkan token.
