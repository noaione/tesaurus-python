# Berkontribusi
Terima kasih telah tertarik untuk melakukan kontribusi terhadap modul tesaurus-python.

Silakan fork terlebih dahulu repository ini, lalu setelah itu Clone repository fork anda.
```bash
$ git clone https://github.com/<username>/tesaurus-python.git
$ cd tesaurus-python
```

Setelah itu buat branch baru untuk kontribusi anda
```bash
$ git checkout -b fitur-baru
```

Setelah itu buat virtualenv dengan nama `venv`
```bash
$ pip3 install -U virtualenv
$ virtualenv venv
```

Aktifkan virtualenv tersebut dengan command `source` di Linux atau jalankan skrip aktivasi di Windows<br>
Linux:
```bash
$ source venv/bin/activate
```
Windows (CMD):
```bat
> venv\Scripts\activate.bat
```
Untuk Powershell, cukup ganti `activate.bat` dengan `activate.ps1`

Setelah itu install semua requirements, termasuk yang requirements-dev.
```
$ pip install -r requirements-dev.txt
```

Silakan lakukan pengembangan anda!

## Mencoba pengembangan
Untuk mencoba code yang telah anda buat, silakan ketik
```
$ pip install -e .
```
Bisa lakukan itu di luar virtualenv maupun di dalam virtualenv, disarankan di luar agar bisa di coba secara global.

## Code Style
Modul ini mengikuti code style [black](https://github.com/psf/black), dengan konfigurasi maksimum 110 huruf per baris.<br>
Modul ini juga mengikuti `import style` [isort](https://github.com/PyCQA/isort) dengan profile black.

## Linting
Modul ini menggunakan flake8 untuk memeriksa atau *linting* code.

Untuk melint, cukup ketik:
```bash
$ flake8
```
Konfigurasi telah diatur dengan file [.flake8](https://github.com/noaione/tesaurus-python/blob/master/.flake8)

## Sebelum membuka PR
Sebelum membuka PR, mohon format kode anda menggunakan black, isort, dan periksa dengan flake8.

```bash
$ black -l 110 .
$ isort -w 110 --profile black tesaurus
$ flake8
```

Semua perintah di atas akan memformat kode, sortir import, lalu memeriksa apakah kode telah cocok dengan spesifikasi PEP8.

### Testing
Setelah itu, mohon test code dengan pytest.<br>
Modul ini menggunakan mock server untuk mensimulasi website.

1. Masuk ke virtualenv terlebih dahulu
2. Di folder utama `(tesaurus-python)`, jalankan server dengan cara
   ```bash
   $ python tests/server.py tests/html
   ```
3. Setelah server jalan, buka console lain dan masuk ke virtualenv
4. Install tesaurus ke virtualenv dengan ketik
   ```bash
   $ pip install -e .
   ```
5. Lalu lakukan tes dengan ketik
   ```bash
   $ pytest tests -v
   ```

Untuk menghentikan server, cukup ketik `CTRL+C`<br>
Pastikan tes sukses dan tidak ada masalah!

Setelah itu, silakan push ke fork anda dan buka PR dengan repository utama ini.

**Selamat berkontribusi!**
