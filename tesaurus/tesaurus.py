"""
:mod:`tesaurus` -- Modul Tesaurus Tematis Python
================================================

.. module:: tesaurus
    :platform: Unix, Windows, Mac
    :synopsis: Modul ini mengandung implementasi scrapper Tesaurus Tematis Kemendikbud
.. moduleauthor:: noaione <noaione0809@gmail.com>
"""

import asyncio
from types import SimpleNamespace

import aiohttp
import requests
from bs4 import BeautifulSoup


class Tesaurus:
    """Sebuah instansi modul Tesaurus"""

    __HOST = "https://tesaurus.kemdikbud.go.id/tematis/lema"

    def __init__(self, sesi: requests.Session = None) -> None:
        """Membuat objek Tesaurus baru

        :param sesi: sesi kustom untuk dipakai
        :type sesi: reequest.Session
        """

        self.kata: str
        self.kelas_kata: str
        self.hasil = []
        self.saran = []

        if isinstance(sesi, (requests.Session, aiohttp.ClientSession)):
            self.sesi = sesi
        else:
            self.sesi = requests.Session()

    def cari(self, kueri: str, kelas_kata: str = None):
        """Mencari kata atau lema di Tesaurus

        :param kueri: kata atau kalimat yang ingin dicari
        :type kueri: str
        :param kelas_kata: kelas kata, defaults to None
        :type kelas_kata: str, optional
        """
        self._reset_data()
        self.kata = kueri
        if isinstance(kelas_kata, str):
            kelas_kata = kelas_kata.lower()
        self.kelas_kata = kelas_kata
        laman_url = self._buat_url()
        laman = self.sesi.get(laman_url)
        self._cek_galat(laman)
        self._buat_entri(laman.text)

    def _reset_data(self):
        """Jangan dipakai, ini merupakan fungsi internal yang akan dipanggil otomatis"""
        self.hasil = []
        self.saran = []
        self.kata = None
        self.kelas_kata = None

    def _buat_url(self):
        """Jangan dipakai, ini merupakan fungsi internal yang akan dipanggil otomatis"""
        base_url = f"{self.__HOST}/{self.kata}"
        valid_kelas = ["adverbia", "konjungsi", "nomina", "numeralia", "partikel", "verba"]
        if isinstance(self.kelas_kata, str):
            if self.kelas_kata not in valid_kelas:
                raise KelasKataTidakDiketahui(self.kelas_kata)
            base_url += f"/{self.kelas_kata}"
        return base_url

    def _cek_galat(self, laman: requests.Response):
        """Jangan dipakai, ini merupakan fungsi internal yang akan dipanggil otomatis"""
        if laman.status_code != 200:
            if laman.status_code == 404:
                raise TidakDitemukan(self.kata, self.kelas_kata)
            raise TerjadiKesalahan()
        not_found_text = "dari semua kelas kata tidak ditemukan"
        if isinstance(self.kelas_kata, str):
            not_found_text = f"dari kelas kata {self.kelas_kata} tidak ditemukan"
        if not_found_text in laman.text:
            raise TidakDitemukan(self.kata, self.kelas_kata)

    def _buat_entri(self, laman: str):
        """Jangan dipakai, ini merupakan fungsi internal yang akan dipanggil otomatis"""
        sup = BeautifulSoup(laman, "html.parser")
        htmlstr = ""
        result_contain = sup.find("div", {"class": "contain"})
        for child in result_contain.children:
            if not htmlstr and child.get("class")[0] == "result-postag":
                htmlstr += str(child)
            elif htmlstr and child.get("class")[0] == "result-postag":
                self.hasil.append(LemaEntri(htmlstr, self.kelas_kata))
                htmlstr = str(child)
            else:
                htmlstr += str(child)


class TesaurusAsync(Tesaurus):
    """Sebuah instansi asynchronous untuk modul Tesaurus"""

    def __init__(self, sesi: aiohttp.ClientSession = None, loop: asyncio.AbstractEventLoop = None) -> None:
        """Membuat objek Tesaurus Baru untuk dipakai di fungsi async.

        :param sesi: Sesi aiohttp kustom yang ingin digunakan, defaults to None
        :type sesi: aiohttp.ClientSession, optional
        """
        super().__init__()
        if not isinstance(loop, asyncio.AbstractEventLoop):
            loop = asyncio.get_event_loop()
        if isinstance(sesi, aiohttp.ClientSession):
            self.sesi = sesi
        else:
            self.sesi = aiohttp.ClientSession(loop=loop)

    async def cari(self, kueri: str, kelas_kata: str):
        self._reset_data()
        self.kata = kueri
        if isinstance(kelas_kata, str):
            kelas_kata = kelas_kata.lower()
        self.kelas_kata = kelas_kata
        laman_url = self._buat_url()
        try:
            req = await self.sesi.get(laman_url)
        except (aiohttp.ClientConnectionError, aiohttp.ClientError, TimeoutError):
            raise TerjadiKesalahan()
        teks = await req.text()
        # Buat namespace yang mirip seperti requests.get()
        laman = SimpleNamespace(text=teks, status_code=req.status)
        self._cek_galat(laman)
        self._buat_entri(teks)


class LemaEntri:
    def __init__(self, hasil_html: str, kelas_kata: str = None):
        self._sup = BeautifulSoup(hasil_html, "html.parser")


class TesaurusGalat(Exception):
    pass


class TerjadiKesalahan(TesaurusGalat):
    def __init__(self) -> None:
        super().__init__(
            "Terjadi kesalahan ketika berkomunikasi dengan website Tesaurus, mohon coba sesaat lagi"
        )


class KelasKataTidakDiketahui(TesaurusGalat):
    def __init__(self, filter_user: str) -> None:
        super().__init__(f"Kelas kata {filter_user} tidak diketahui.")


class TidakDitemukan(TesaurusGalat):
    def __init__(self, kata: str, kelas_kata: str = None) -> None:
        err_msg = f"Tidak dapat menemukan kata {kata} pada "
        if isinstance(kelas_kata, str):
            err_msg += f"kelas kata {kelas_kata}."
        else:
            err_msg += "semua kelas kata."

        super().__init__(err_msg)
