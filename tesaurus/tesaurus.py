"""
:mod:`tesaurus` -- Modul Tesaurus Tematis Python
================================================

.. module:: tesaurus
    :platform: Unix, Windows, Mac
    :synopsis: Modul ini mengandung implementasi scrapper Tesaurus Tematis Kemendikbud
.. moduleauthor:: noaione <noaione0809@gmail.com>
"""

import requests
from bs4 import BeautifulSoup


class Tesaurus:
    """Sebuah hasil lema di Tesaurus Tematis"""

    __HOST = "https://tesaurus.kemdikbud.go.id/tematis/lema"

    def __init__(self, kueri: str, kelas_kata: str = None) -> None:
        """Membuat objek Tesaurus baru berdasarkan kueri yang diberikan.

        :param kueri: Kata kunci pencarian
        :type kueri: str
        :param loop: Sebuah event loop asyncio
        """

        self.nama = kueri
        if isinstance(kelas_kata, str):
            kelas_kata = kelas_kata.lower()
        self.kelas_kata = kelas_kata
        self.hasil = []
        self.saran = []

        self.sesi = requests.Session()
        laman_url = self._buat_url()
        laman = self.sesi.get(laman_url)
        self._cek_galat(laman)
        self._buat_entri(laman.text)

    def _buat_url(self):
        base_url = f"{self.__HOST}/{self.nama}"
        valid_kelas = ["adverbia", "konjungsi", "nomina", "numeralia", "partikel", "verba"]
        if isinstance(self.kelas_kata, str):
            if self.kelas_kata not in valid_kelas:
                raise TesaurusKelasTidakDiketahui(self.kelas_kata)
            base_url += f"/{self.kelas_kata}"
        return base_url

    def _cek_galat(self, laman: requests.Response):
        if laman.status_code != 200:
            raise TerjadiKesalahan()
        not_found_text = "dari semua kelas kata tidak ditemukan"
        if isinstance(self.kelas_kata, str):
            not_found_text = f"dari kelas kata {self.kelas_kata} tidak ditemukan"
        if not_found_text in laman.text:
            raise TidakDitemukan(self.nama, self.kelas_kata)

    def _buat_entri(self, laman: str):
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


class TesaurusKelasTidakDiketahui(TesaurusGalat):
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
