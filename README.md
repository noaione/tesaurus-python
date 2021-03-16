<p align="center">
  <img align="middle" width="300" height="300" src="https://raw.githubusercontent.com/noaione/tesaurus-python/master/assets/logo.png">
</p>
<h1 align="center">
    tesaurus-python
</h1>
<p align="center"><b>Versi 0.1.2</b><br>Sebuah modul Python untuk mengambil informasi Tesaurus dari Tesaurus Tematis Kemdikbud (http://tesaurus.kemdikbud.go.id/)
</p>

<div align="center">
<a href="https://pypi.org/project/tesaurus/"><img alt="PyPI" src="https://img.shields.io/pypi/v/tesaurus"></a><a href="https://pypi.org/project/tesaurus/"> <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/tesaurus"></a><a href="https://github.com/noaione/tesaurus-python/actions/workflows/test.yml"> <img src="https://github.com/noaione/tesaurus-python/actions/workflows/test.yml/badge.svg" alt="Test CI"></a><a href="https://github.com/noaione/tesaurus-python/blob/master/LICENSE"> <img src="https://img.shields.io/github/license/noaione/tesaurus-python" alt="LICENSE: MIT"></a><a href="https://coveralls.io/github/noaione/tesaurus-python?branch=master"> <img src="https://coveralls.io/repos/github/noaione/tesaurus-python/badge.svg?branch=master" alt="Coverage Status" /></a><a href="https://github.com/psf/black"> <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style: black"></a>
</div>

---

## Fitur
- Support Asynchrounous agar bisa digunakan di fungsi async ([`TesaurusAsync`](https://github.com/noaione/tesaurus-python/blob/master/tesaurus/tesaurus.py#L223))
- CLI Support, agar tidak usah import manual
- Batasi hasil ke kelas kata tertentu
- Lihat hasil terkait jika tersedia.

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
pip install tesaurus
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
tesaurus-python juga dapat diakses melalui CLI, cukup install via PyPI dan ketik `tesaurus`<br>
Anda bisa melihat bantuan dengan menulis `tesaurus -h`.

```bash
$ tesaurus
usage: tesaurus [-h] [-V] [-t] [-k {adverbia,konjungsi,nomina,numeralia,partikel,verba}] [-j] [-i N] kata

Mencari informasi tesaurus dari Tesaurus Tematis

positional arguments:
  kata                  Kata atau kalimat yang ingin dicari

optional arguments:
  -h, -b, --help, --bantuan
                        tampilkan pesan bantuan ini dan keluar
  -V, --versi, --version
                        Melihat versi Tesaurus dan keluar
  -t, ---dengan-terkait
                        Tampilkan hasil terkait (bila ada)
  -k {adverbia,konjungsi,nomina,numeralia,partikel,verba}, --kelas-kata {adverbia,konjungsi,nomina,numeralia,partikel,verba}
                        Batasi hasil ke kelas kata tertentu
  -j, --json            Tampilkan hasil dengan format JSON
  -i N, --indentasi N   gunakan identasi sebanyak N untuk format JSON
```

Untuk mencari sebuah kata cukup tulis kata tersebut setelah `tesaurus`
```bash
$ tesaurus makan
makan
[adjektiva]
 marah: bengis, berang, berangasan, berangsang, berangus, berapi-api, burangsang, gemas, geram, geregetan, gondok, gusar, hangus dada, hangus hati, jaki, jengkel, kamun, keki, makan bawang, meluap, membayang, mendidih, mengkal, mengkal hati, meradang, merah telinga, merajuk, meruak, murik, murka, naik darah, naik garam, naik palak, naik pitam, naik seh, naik setrum, palak, panas hati, pedar, pegal hati, redut, rongseng, sengiang, serangsang, sewot
 malas: celih, celika, cuai, culas, gontai, kelesah, lamban, lambat, lemah, lengah, lesu, loyo, lundung, makan tidur, rengsa, sambalewa, segan, seleder, taufah, teledor, wegah (cak)
 makanan: belalah, bosor makan, demap, gelojoh, kemaruk, kenyir, lahap, lalah, majuh, rakus

[nomina]
 perdu: (perdu hias) alamanda, bugenvil, gambir hutan, kacapiring, krisantemum, mawar, melati, merak, nona makan sirih, nusa indah, oleander, puding, ros
 bunga: akasia, alamanda, amarilis, anggrek, anyelir, aster, azalea, bakung, begonia, bugenvil, bunga bangkai, bunga gambir, bunga kemboja, bunga kana, bunga kenop, bunga landak, bunga lili, bunga matahari, bunga merak, bunga pagoda, bunga raya, bunga sepatu, bunga tahi ayam, bunga tanjung, bunga telang, bungur, cempaka, dahlia, flamboyan, gandasuli, gladiol, hortensia, jengger ayam, kacapiring, kaktus, kamelia, kecubung, kedawung, kembang asoka, kembang goyang, kembang sepatu, kemboja, kemuning, kenanga, kenikir, krisan, lavender, mawar, melati jepang, melati, nona makan sirih, nusa indah, oleander, raflesia, ros, sedap malam, serigading, seroja, tapak dara, teratai, terung susu, tulip, violet
 sembuh: pantang (makan), diet, puasa, vegetarian
 istirahat: jeda, rehat kopi, selingan, waktu istirahat, waktu rehat, isoma (istirahat, salat, makan siang)
 nafsu: (hawa nafsu) nafsu amarah, nafsu bejat, nafsu berahi, nafsu iblis, nafsu lawamah, nafsu makan, nafsu mutmainah, nafsu seks, nafsu setan, nafsu syahwat
 nafsu: (nafsu makan) begah, berliur, haus, kenyang, lahap, lapar, selera
 permusuhan: musuh bebuyutan, musuh dalam selimut, musuh lama, musuh turun-temurun, pagar makan tanaman
 doa: (islam) doa harian, doa bangun tidur, doa keluar kamar mandi, doa masuk pasar, doa ketika mendapat kesenangan, doa ketika mendengar geledek, doa ketika tertimpa musibah, doa membesuk orang sakit, doa pagi hari, doa sebelum bepergian, doa sebelum belajar, doa sebelum makan, doa sebelum masuk kamar mandi, doa sebelum tidur, doa selesai belajar, doa sesudah makan, doa sore hari, doa ratib, wirid, zikir, tahlil, talkin, doa kunut, doa selamat, khotbah, salat
 tempat kerja: pasar swalayan, pasar tradisional, toko, toko serbaada, toko serbaneka, belerong, dukan, gerai, kedai, kios, lapak, los, kafe, kafetaria, kantin, lepau, resto (cak), restoran, rumah makan, warung, warung tenda, warteg (warung tegal), butik, galeri, studio
 perdagangan: (tempat usaha) butik, gerai, hipermarket, kedai, kios, lapak, pasar, pasar swalayan, supermarket, toko, toko serba ada (toserba), warung, kantin, kafe, kafetaria, lepau, restoran, rumah makan, warteg (warung tegal), bazar, eksibisi, ekspo, fair, pekan raya, pameran, pasar murah
 bangunan: (rumah makan dan minum) bar, depot, kafe, kafetaria, kantin, kedai kopi, kedai nasi, kedai susu, lapo tuak, restoran, restorasi, rumah makan, warung nasi
 permukiman: (kamar) barak, bilik, petak, ruang, kamar kecil, kamar keluarga, kamar makan, kamar mandi, kamar tamu, kamar tidur, ruang cuci, ruang keluarga, ruang makan, ruang tamu, ruang tengah, gudang
 peranti makan: (piring) piring cembung, piring datar, piring ikan, piring kue, piring lauk, piring makan, piring roti, piring salad
 peranti makan: (sendok) sendok bebek, sendok bubur, sendok kopi, sendok es krim, sendok kue, sendok makan, sendok nasi, sendok sayur, sendok sirup, sendok sup, sendok tambul, sendok teh
 peranti makan: (garpu) garpu ikan, garpu kue, garpu makan, garpu salad, garpu tiram
 peranti makan: (pisau) pisau buah, pisau bistik, pisau daging, pisau dapur, pisau ikan, pisau keju, pisau kue, pisau makan, pisau meja, pisau mentega, pisau roti, pisau stik
 peranti makan: (pengelap) lap, serbet, tisu, tisu gulung, tisu makan, waslap
 pembersih: (lap) lap dapur, lap kaki, lap kursi, lap lantai, lap piring, lap makan, lap meja, serbet, keset
 mebel dan perabot elektronik: (lemari) lemari baju, lemari besi, lemari buku, lemari dapur, lemari es, lemari gantung, lemari hias, lemari kaca, lemari makan, lemari pajangan, lemari pakaian, lemari pendingin, lemari tanam, lemari dua pintu, lemari satu pintu, lemari tiga pintu, sepen
 mebel dan perabot elektronik: (kursi) kursi bar, kursi berlengan, kursi goyang, kursi lipat, kursi makan, kursi malas, kursi panjang, kursi roda, kursi setel, kursi susun, kursi taman
 mebel dan perabot elektronik: (meja) meja belajar, meja dapur, meja lipat, meja makan, meja modular, meja plastik, meja putar, meja rias, meja sorong, meja sudut, meja susun, meja tamu, meja tulis, nakas
 tata boga: (waktu makan) makan pagi, sarapan, makan siang, makan malam
 tata boga: kafe, kafetaria, kantin, lapo, lepau, restoran, rumah makan, kedai, warung
 makanan: nafsu makan, selera makan, rasa lapar, kelaparan
 makanan: (kekenyangan) kebanyakan (makan), kepenuhan
 makanan: ahli makan, pelahap, pencicip, perut karet (ki), tukang makan
 beternak: (penyakit sapi) cacingan (cak), diare, kembung, kurang nafsu makan, penyakit kuku dan mulut, penyakit sapi gila
```

Bisa juga kita batasi ke kelas kata tertentu dengan parameter `-k` atau `--kelas-kata`

```bash
$ tesaurus makan -k adjektiva
makan
[adjektiva]
 marah: bengis, berang, berangasan, berangsang, berangus, berapi-api, burangsang, gemas, geram, geregetan, gondok, gusar, hangus dada, hangus hati, jaki, jengkel, kamun, keki, makan bawang, meluap, membayang, mendidih, mengkal, mengkal hati, meradang, merah telinga, merajuk, meruak, murik, murka, naik darah, naik garam, naik palak, naik pitam, naik seh, naik setrum, palak, panas hati, pedar, pegal hati, redut, rongseng, sengiang, serangsang, sewot
 malas: celih, celika, cuai, culas, gontai, kelesah, lamban, lambat, lemah, lengah, lesu, loyo, lundung, makan tidur, rengsa, sambalewa, segan, seleder, taufah, teledor, wegah (cak)
 makanan: belalah, bosor makan, demap, gelojoh, kemaruk, kenyir, lahap, lalah, majuh, rakus
```

Jika ingin mendapatkan data terkait, bisa juga memberikan parameter `-t` atau `--dengan-terkait`

```bash
$ tesaurus makan -t -k adjektiva
```

Jika ingin mendapatkan dengan hasil JSON, bisa dengan memberikan parameter `-j` atau `--json`, untuk memberikan indentasi, cukup tambahkan param `-i N` atau `--indentasi N` di mana `N` adalah angka.

```bash
$ tesaurus makan -k -j
{"kata": "makan", "pranala": "https://tesaurus.kemdikbud.go.id/tematis/lema/makan/adjektiva", "entri": [{"kelas": "adjektiva", "entri": [{"label": "marah", "sublabel": null, "lema": ["bengis", "berang", "berangasan", "berangsang", "berangus", "berapi-api", "burangsang", "gemas", "geram", "geregetan", "gondok", "gusar", "hangus dada", "hangus hati", "jaki", "jengkel", "kamun", "keki", "makan bawang", "meluap", "membayang", "mendidih", "mengkal", "mengkal hati", "meradang", "merah telinga", "merajuk", "meruak", "murik", "murka", "naik darah", "naik garam", "naik palak", "naik pitam", "naik seh", "naik setrum", "palak", "panas hati", "pedar", "pegal hati", "redut", "rongseng", "sengiang", "serangsang", "sewot"]}, {"label": "malas", "sublabel": null, "lema": ["celih", "celika", "cuai", "culas", "gontai", "kelesah", "lamban", "lambat", "lemah", "lengah", "lesu", "loyo", "lundung", "makan tidur", "rengsa", "sambalewa", "segan", "seleder", "taufah", "teledor", "wegah (cak)"]}, {"label": "makanan", "sublabel": null, "lema": ["belalah", "bosor makan", "demap", "gelojoh", "kemaruk", "kenyir", "lahap", "lalah", "majuh", "rakus"]}]}]}
```

```bash
$ tesaurus makan -k -j -i 2
{
  "kata": "makan",
  "pranala": "https://tesaurus.kemdikbud.go.id/tematis/lema/makan/adjektiva",
  "entri": [
    {
      "kelas": "adjektiva",
      "entri": [
        {
          "label": "marah",
          "sublabel": null,
          "lema": [
            "bengis",
            "berang",
            "berangasan",
            "berangsang",
            "berangus",
            "berapi-api",
            "burangsang",
            "gemas",
            "geram",
            "geregetan",
            "gondok",
            "gusar",
            "hangus dada",
            "hangus hati",
            "jaki",
            "jengkel",
            "kamun",
            "keki",
            "makan bawang",
            "meluap",
            "membayang",
            "mendidih",
            "mengkal",
            "mengkal hati",
            "meradang",
            "merah telinga",
            "merajuk",
            "meruak",
            "murik",
            "murka",
            "naik darah",
            "naik garam",
            "naik palak",
            "naik pitam",
            "naik seh",
            "naik setrum",
            "palak",
            "panas hati",
            "pedar",
            "pegal hati",
            "redut",
            "rongseng",
            "sengiang",
            "serangsang",
            "sewot"
          ]
        },
        {
          "label": "malas",
          "sublabel": null,
          "lema": [
            "celih",
            "celika",
            "cuai",
            "culas",
            "gontai",
            "kelesah",
            "lamban",
            "lambat",
            "lemah",
            "lengah",
            "lesu",
            "loyo",
            "lundung",
            "makan tidur",
            "rengsa",
            "sambalewa",
            "segan",
            "seleder",
            "taufah",
            "teledor",
            "wegah (cak)"
          ]
        },
        {
          "label": "makanan",
          "sublabel": null,
          "lema": [
            "belalah",
            "bosor makan",
            "demap",
            "gelojoh",
            "kemaruk",
            "kenyir",
            "lahap",
            "lalah",
            "majuh",
            "rakus"
          ]
        }
      ]
    }
  ]
}
```

## Berkontribusi
Lihat [CONTRIBUTING.md](https://github.com/noaione/tesaurus-python/blob/master/CONTRIBUTING.md)

## Perubahan
Lihat [CHANGELOG.md](https://github.com/noaione/tesaurus-python/blob/master/CHANGELOG.md)

## Lisensi
Modul ini didistribusikan dengan lisensi [MIT](https://github.com/noaione/tesaurus-python/blob/master/LICENSE).

## Penutup
Projek ini dibuat untuk keperluan pribadi dan tidak ada afiliasi dengan Kemdikbud. Projek ini mengambil inspirasi dari [kbbi-python](https://github.com/laymonage/kbbi-python) oleh laymonage.

Logo yang dipakai di bagian atas header merupakan [logo favicon](http://tesaurus.kemdikbud.go.id/tematis/styles/img/favicon.ico) dari website [Tesaurus Tematis](http://tesaurus.kemdikbud.go.id/tematis/), logo dibuat ulang di Photoshop dikarenakan resolusi yang rendah. Kredit logo asli merupakan hak milik Kemdikbud.