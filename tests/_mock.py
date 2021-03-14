from tesaurus import KelasKataTidakDiketahui, Tesaurus, TesaurusAsync


class MockTesaurus(Tesaurus):
    HOST = "http://localhost:4000"
    _HOST = Tesaurus.HOST

    def __init__(self) -> None:
        super().__init__()

    def _buat_url(self):
        """Jangan dipakai, ini merupakan fungsi internal yang akan dipanggil otomatis"""
        base_url = f"{self.HOST}/{self.kata}"
        valid_kelas = ["adjektiva", "adverbia", "konjungsi", "nomina", "numeralia", "partikel", "verba"]
        if isinstance(self.kelas_kata, str):
            if self.kelas_kata not in valid_kelas:
                self._on_queue = False
                self._logger.error(f"Kelas kata {self.kelas_kata} tidak diketahui")
                raise KelasKataTidakDiketahui(self.kelas_kata)
            base_url += f"/{self.kelas_kata}"
        return base_url + ".html"


class MockTesaurusAsync(TesaurusAsync):
    HOST = "http://localhost:4000"
    _HOST = Tesaurus.HOST

    def __init__(self) -> None:
        super().__init__()
