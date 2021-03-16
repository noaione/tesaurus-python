"""
:mod:`tesaurus` -- Modul Tesaurus Tematis Python
================================================

.. module:: tesaurus
    :platform: Unix, Windows, Mac
    :synopsis: Modul ini mengandung implementasi scrapper Tesaurus Tematis Kemendikbud
.. moduleauthor:: noaione <noaione0809@gmail.com>
"""

import asyncio
import logging
import typing as t
from types import SimpleNamespace

import aiohttp
import bs4
import requests

__author__ = "noaione"
__author_mail__ = "noaione0809@gmail.com"
__version__ = "0.1.2"


class Lema(t.NamedTuple):
    label: str
    sublabel: t.Union[str, None]
    lema: t.List[str]

    def to_dict(self):
        """Ubah NamedTuple Lema ke dictionary"""
        return {"label": self.label, "sublabel": self.sublabel, "lema": self.lema}


class Tesaurus:
    """Objek utama modul Tesaurus"""

    HOST = "https://tesaurus.kemdikbud.go.id/tematis/lema"

    def __init__(self, sesi: requests.Session = None) -> None:
        """Membuat objek Tesaurus baru

        :param sesi: sesi kustom untuk dipakai
        :type sesi: reequest.Session
        """

        self._logger = logging.getLogger("tesaurus.Tesaurus")

        self.kata: str = None
        self.kelas_kata: str = None
        self._entri: t.List[LemaEntri] = []
        self._terkait: t.List[LemaEntri] = []

        self._on_queue = False

        if isinstance(sesi, (requests.Session, aiohttp.ClientSession)):
            self.sesi = sesi
        else:
            self.sesi = requests.Session()

    @property
    def entri(self):
        return self._entri

    @property
    def terkait(self):
        return self._terkait

    def tutup(self):
        """Tutup koneksi dan bersihkan queue!"""
        import time

        while self._on_queue:
            if not self._on_queue:  # pragma: nocover
                break
            time.sleep(0.2)  # pragma: nocover
        self.sesi.close()

    def cari(self, kueri: str, kelas_kata: str = None):
        """Mencari kata atau lema di Tesaurus

        :param kueri: kata atau kalimat yang ingin dicari
        :type kueri: str
        :param kelas_kata: kelas kata, defaults to None
        :type kelas_kata: str, optional
        """
        self._logger.debug(f"Mencari `{kueri}` dengan kelas kata `{kelas_kata}`")
        if kueri == self.kata and kelas_kata == self.kelas_kata:
            self._logger.debug("Terdapat cache dari pencarian sebelumnya, silakan gunakan cache")
            return
        self._on_queue = True
        self._reset_data()
        self.kata = kueri
        if isinstance(kelas_kata, str):
            kelas_kata = kelas_kata.lower()
        self.kelas_kata = kelas_kata
        laman_url = self._buat_url()
        self._logger.debug(f"Meminta pranala {laman_url}")
        laman = self.sesi.get(laman_url)
        self._cek_galat(laman)
        try:
            self._logger.debug("Mengumpulkan hasil...")
            self._buat_entri(laman.text)
            self._buat_terkait(laman.text)
        except TesaurusGalat as errtg:
            self._on_queue = False
            self._logger.error(f"Sebuah galat terjadi, {str(errtg)}")
            raise TesaurusGalat(str(errtg))
        self._on_queue = False

    def _reset_data(self):
        """Jangan dipakai, ini merupakan fungsi internal yang akan dipanggil otomatis"""
        self._entri = []
        self._terkait = []
        self.kata = None
        self.kelas_kata = None

    def _buat_url(self):
        """Jangan dipakai, ini merupakan fungsi internal yang akan dipanggil otomatis"""
        base_url = f"{self.HOST}/{self.kata}"
        valid_kelas = ["adjektiva", "adverbia", "konjungsi", "nomina", "numeralia", "partikel", "verba"]
        if hasattr(self, "kelas_kata") and isinstance(self.kelas_kata, str):
            if self.kelas_kata not in valid_kelas:
                self._on_queue = False
                self._logger.error(f"Kelas kata {self.kelas_kata} tidak diketahui")
                raise KelasKataTidakDiketahui(self.kelas_kata)
            base_url += f"/{self.kelas_kata}"
        return base_url

    def _cek_galat(self, laman: requests.Response):
        """Jangan dipakai, ini merupakan fungsi internal yang akan dipanggil otomatis"""
        self._logger.debug("Memerika galat pada pranala tadi...")
        if laman.status_code != 200:
            self._on_queue = False
            if laman.status_code == 404:
                self._logger.error("Tidak dapat hasil")
                raise TidakDitemukan(self.kata, self.kelas_kata)
            self._logger.error("Terjadi kesalahan ketika berkomunikasi dengan Tesaurus Tematis")
            raise TerjadiKesalahan()
        not_found_text = "dari semua kelas kata tidak ditemukan"
        if isinstance(self.kelas_kata, str):
            not_found_text = f"dari kelas kata {self.kelas_kata} tidak ditemukan"
        if not_found_text in laman.text:
            self._on_queue = False
            self._logger.error("Tidak ada hasil")
            raise TidakDitemukan(self.kata, self.kelas_kata)

    def _buat_entri(self, laman: str):
        """Jangan dipakai, ini merupakan fungsi internal yang akan dipanggil otomatis"""
        sup = bs4.BeautifulSoup(laman, "html.parser")
        htmlstr = ""
        result_contain = sup.find("div", {"class": "contain"})
        for child in result_contain.children:
            if not htmlstr and child.get("class")[0] == "result-postag":
                htmlstr += str(child)
            elif htmlstr and child.get("class")[0] == "result-postag":
                self._entri.append(LemaEntri(htmlstr, self.kelas_kata))
                htmlstr = str(child)
            else:
                htmlstr += str(child)
        self._entri.append(LemaEntri(htmlstr, self.kelas_kata))

    def _buat_terkait(self, laman: str):
        """Jangan dipakai, ini merupakan fungsi internal yang akan dipanggil otomatis"""
        sup = bs4.BeautifulSoup(laman, "html.parser")
        htmlstr = ""
        result_related = sup.find("div", {"class": "related"})
        if result_related:
            for child in result_related.children:
                if child.get("class") and child.get("class")[0] == "related-result":
                    continue
                if not htmlstr and child.get("class")[0] == "result-postag":
                    htmlstr += str(child)
                elif htmlstr and child.get("class")[0] == "result-postag":
                    try:
                        self._terkait.append(LemaEntri(htmlstr, self.kelas_kata))
                    except TesaurusGalat:
                        self._logger.warning("Gagal memproses salah satu hasil terkait, mengabaikannya...")
                    htmlstr = str(child)
                else:
                    htmlstr += str(child)
            try:
                self._terkait.append(LemaEntri(htmlstr, self.kelas_kata))
            except TesaurusGalat:
                self._logger.warning("Gagal memproses salah satu hasil terkait, mengabaikannya...")

    def serialisasi(self) -> dict:
        """Serialisasi hasil menjadi sebuah objek.

        :return: Objek/Dictionary dari Kata yang dicari
        :rtype: dict
        """
        if self.kata is None:
            raise TesaurusGalat("Tidak ada kata yang sedang dicari.")
        pranala = self._buat_url()
        tesaurus = {
            "kata": self.kata,
            "pranala": pranala,
            "entri": [entri.serialisasi() for entri in self._entri],
            "terkait": [entri.serialisasi() for entri in self._terkait],
        }
        return tesaurus

    def __str__(self, terkait=False) -> str:
        if self.kata is None:
            return "Tidak ada kata yang sedang dicari."
        hasil = f"{self.kata}\n"
        if self._entri:
            hasil += "\n\n".join(str(entri) for entri in self._entri)
        else:
            hasil += "Tidak ada hasil."
        if self._terkait and terkait:
            hasil += "\n\n* Hasil terkait:\n"
            hasil += "\n\n".join(str(entri) for entri in self._terkait)
        return hasil

    def __repr__(self) -> str:
        if not self.kata:
            return "<Tesaurus: TidakAda>"
        hasil = self.kata
        if self.kelas_kata is not None:
            hasil += f" [{self.kelas_kata}]"
        return f"<Tesaurus: {hasil}>"


class TesaurusAsync(Tesaurus):
    """Objek utama versi asynchronous untuk modul Tesaurus"""

    def __init__(self, sesi: aiohttp.ClientSession = None, loop: asyncio.AbstractEventLoop = None) -> None:
        """Membuat objek Tesaurus Baru untuk dipakai di fungsi async.

        :param sesi: Sesi aiohttp kustom yang ingin digunakan, defaults to None
        :type sesi: aiohttp.ClientSession, optional
        """
        super().__init__()
        if not isinstance(loop, asyncio.AbstractEventLoop):
            loop = asyncio.get_event_loop()
        self._logger = logging.getLogger("tesaurus.TesaurusAsync")
        self._loop = loop
        if isinstance(sesi, aiohttp.ClientSession):
            self.sesi = sesi
        else:
            self.sesi = aiohttp.ClientSession(loop=loop)

    async def tutup(self):
        while self._on_queue:
            if not self._on_queue:  # pragma: nocover
                break
            await asyncio.sleep(0.2)  # pragma: nocover
        await self.sesi.close()

    async def cari(self, kueri: str, kelas_kata: str = None):
        self._logger.debug(f"Mencari `{kueri}` dengan kelas kata `{kelas_kata}`")
        if kueri == self.kata and kelas_kata == self.kelas_kata:
            self._logger.debug("Terdapat cache dari pencarian sebelumnya, silakan gunakan cache")
            return
        self._on_queue = True
        self._reset_data()
        self.kata = kueri
        if isinstance(kelas_kata, str):
            kelas_kata = kelas_kata.lower()
        self.kelas_kata = kelas_kata
        laman_url = self._buat_url()
        try:
            self._logger.debug(f"Meminta pranala {laman_url}")
            req = await self.sesi.get(laman_url)
        except (aiohttp.ClientConnectionError, aiohttp.ClientError, TimeoutError):  # pragma: nocover
            self._logger.error("Terjadi kesalahan ketika berkomunikasi dengan Tesaurus Tematis")
            self._on_queue = False
            raise TerjadiKesalahan()
        teks = await req.text()
        # Buat namespace yang mirip seperti requests.get()
        laman = SimpleNamespace(text=teks, status_code=req.status)
        self._cek_galat(laman)
        try:
            self._logger.debug("Mengumpulkan hasil...")
            self._buat_entri(teks)
        except TesaurusGalat as errtg:
            self._on_queue = False
            self._logger.error(f"Sebuah galat terjadi, {str(errtg)}")
            raise TesaurusGalat(str(errtg))
        self._on_queue = False

    def __del__(self):
        if not self.sesi.closed:
            self._loop.run_until_complete(self.sesi.close())

    def __repr__(self) -> str:
        if not self.kata:
            return "<TesaurusAsync: TidakAda>"
        hasil = self.kata
        if self.kelas_kata is not None:
            hasil += f" [{self.kelas_kata}]"
        return f"<TesaurusAsync: {hasil}>"


class LemaEntri:
    """Objek entri untuk koleksi lema pada sebuah kelas kata

    Objek ini tidak dimakud untuk dibuat oleh pengguna.
    """

    def __init__(self, hasil_html: str, kelas_kata: str = None):
        """Buat objek Entri baru

        Tidak dimaksud untuk dibuat oleh pengguna.

        :param hasil_html: HTML yang mengandung <div> dengan kelas result-set
                           dan result-postag jika ada
        :type hasil_html: str
        :param kelas_kata: kelas kata pengganti jika result-postag tidak ada, defaults to None
        :type kelas_kata: str, optional
        :raises TesaurusGalat: Jika tidak ada result-postag di HTML dan kelas_kata tidak diberikan.s
        """
        self._sup = bs4.BeautifulSoup(hasil_html, "html.parser")

        self.kelas_kata: str
        self._init_kelas(kelas_kata)
        self._entri: t.List[Lema] = []
        result_sets = self._sup.find_all("div", {"class": "result-set"})
        if result_sets:
            self._init_hasil(result_sets)

    @property
    def entri(self) -> t.List[Lema]:
        """Koleksi Lema yang sudah diproses.

        :return: koleksi lema
        :rtype: t.List[Lema]
        """
        return self._entri

    def _init_kelas(self, kelas_kata: str = None):
        postag: t.Union[bs4.element.Tag, None] = self._sup.find("div", {"class": "result-postag"})
        if postag is None and kelas_kata is None:
            raise TesaurusGalat("Gagal memproses entri, tidak ada kelas kata yang bisa ditemukan!")
        elif postag is None:
            self.kelas_kata = kelas_kata
        else:
            self.kelas_kata = postag.findChild("i").text.rstrip()

    def _init_hasil(self, result_sets: t.List[bs4.element.Tag]):
        for hasil in result_sets:
            tabel = {}
            label = hasil.find("div", {"class": "article-label"}).findChild("a").text.rstrip().lower()
            tabel["label"] = label
            tabel["sublabel"] = None
            semua_lema: bs4.element.Tag = hasil.find("div", {"class": "one-par-content"})
            koleksi_lema = []
            if semua_lema is not None:
                for lema in semua_lema.children:
                    if not lema.name:
                        continue
                    if lema.name != "a":
                        continue
                    if lema.get("class") and lema.get("class")[0] == "lemma-super":
                        tabel["sublabel"] = lema.text.rstrip().lower()
                        continue
                    koleksi_lema.append(lema.text.rstrip().lower())
            tabel["lema"] = koleksi_lema
            self._entri.append(Lema(**tabel))

    def serialisasi(self) -> t.Dict[str, t.Any]:
        """Serialisasi hasil ke objek dictionary

        :return: hasil serilisasi
        :rtype: t.Dict[str, t.Any]
        """
        entri_serialized = [entri.to_dict() for entri in self._entri]
        return {"kelas": self.kelas_kata, "entri": entri_serialized}

    def __str__(self):
        hasil = f"[{self.kelas_kata}]\n"
        if not self._entri:
            hasil += "Tidak ada entri"
            return hasil
        for entri in self._entri:
            hasil += f" {entri.label}:"
            if entri.sublabel:
                hasil += f" ({entri.sublabel})"
            hasil += f" {', '.join(entri.lema)}\n"
        return hasil.rstrip("\n")

    def __repr__(self) -> str:
        return f"<LemaEntri: {self.kelas_kata}, {len(self._entri)} Entri>"


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
