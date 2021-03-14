<p align="center">
  <img align="middle" width="300" height="300" src="https://raw.githubusercontent.com/noaione/tesaurus-python/master/assets/logo.png">
</p>
<h1 align="center">
    tesaurus-python
</h1>
<p align="center"><b>Versi 0.1.0</b><br>Sebuah modul Python untuk mengambil informasi Tesaurus dari Tesaurus Tematis Kemendikbud (http://tesaurus.kemdikbud.go.id/)
</p>

---

## Fitur
- [x] Support Asynchrounous agar bisa digunakan di fungsi async ([`TesaurusAsync`](https://github.com/noaione/tesaurus-python/blob/master/tesaurus/tesaurus.py#L131))
- [ ] CLI Support, agar tidak usah import manual
- [x] Batasi hasil ke kelas kata tertentu

## Requirements
- Python 3.6+
- [requests](https://pypi.org/project/requests/)
- [aiohttp](https://pypi.org/project/aiohttp/)
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)

Jika anda ingin berkontribusi, anda juga butuh:
- flake8
- isort
- black

## Instalasi
### Melalui pypi
```bash
pip install ----
```

### Manual
1. Clone repository ini
2. Install requirements yaitu ([`aiohttp`](https://pypi.org/project/aiohttp/), [`requests`](https://pypi.org/project/requests/), dan [`beautifulsoup4`](https://pypi.org/project/beautifulsoup4/)) atau dengan `pip install -r requirements.txt`
3. Pindahkan file [`tesaurus.py`](https://github.com/noaione/tesaurus-python/blob/master/tesaurus/tesaurus.py) ke folder yang diinginkan.

## Pengunaan
### Sebagai modul
tesaurus-python dapat diimport manual sebagai modul sendiri, cukup import seperti ini objek `Tesaurus` atau `TesaurusAsync` jika ingin menggunakan versi async
```py
from tesaurus import Tesaurus

te = Tesaurus()
te.cari("makan")
print(te)
```

Objek utama dapat menerima session dari user dengan cukup memberikan objek `requests.Session` untuk `Tesaurus` atau `aiohttp.ClientSession` untuk `TesaurusAsync`.

```py
import requests
from tesaurus import Tesaurus

sesi = requests.Session()
sesi.headers.update({"User-Agent": ".............."})

te = Tesaurus(sesi)
te.cari("makan")
print(te)
```

Jika anda developer dan ingin menggunakan format dictionary, cukup panggil fungsi `.serialisasi()`

```py
import json
from tesaurus import Tesaurus

te = Tesaurus(sesi)
te.cari("makan")
print(json.dumps(te.serialisasi(), indent=2))
```

### Melalui CLI
Akan ditulis

## Berkontribusi
Lihat ...

## Lisensi
Modul ini didistribusikan dengan lisensi [MIT](https://github.com/noaione/tesaurus-python/blob/master/LICENSE).

## Penafian
Akan ditulis
