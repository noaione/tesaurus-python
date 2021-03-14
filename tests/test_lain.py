import asyncio
from types import SimpleNamespace

import aiohttp
import pytest
import requests
from tesaurus import KelasKataTidakDiketahui, Lema, LemaEntri, TerjadiKesalahan, Tesaurus, TidakDitemukan
from tesaurus.tesaurus import TesaurusAsync

SAMPLE_HTML_1 = """<div class="related"><div class="result-set"><div class="article-label col-lg-2 col-md-2"><a href="http://tesaurus.kemdikbud.go.id/tematis/artikel/Peranti_Makan">PERANTI MAKAN</a></div><div class="one-par col-lg-9 col-md-9"><div class="one-par-content"><a href="http://tesaurus.kemdikbud.go.id/tematis/lema/menempatkan" class="lemma-ordinary">menempatkan</a>, <a href="http://tesaurus.kemdikbud.go.id/tematis/lema/menyajikan" class="lemma-ordinary">menyajikan</a>, <a href="http://tesaurus.kemdikbud.go.id/tematis/lema/menyimpan" class="lemma-ordinary">menyimpan</a>, <a href="http://tesaurus.kemdikbud.go.id/tematis/lema/mewadahi" class="lemma-ordinary">mewadahi</a></div></div></div></div>"""  # noqa: E501
SAMPLE_HTML_2 = """<div class="related"><div class="result-set"><div class="article-label col-lg-2 col-md-2"><a href="http://tesaurus.kemdikbud.go.id/tematis/artikel/Peranti_Makan">PERANTI MAKAN</a></div><div class="one-par col-lg-9 col-md-9"><div class="one-par-content"><a href="http://tesaurus.kemdikbud.go.id/tematis/lema/menempatkan" class="lemma-ordinary">menempatkan</a>, <a href="http://tesaurus.kemdikbud.go.id/tematis/lema/menyajikan" class="lemma-ordinary">menyajikan</a>, <a href="http://tesaurus.kemdikbud.go.id/tematis/lema/menyimpan" class="lemma-ordinary">menyimpan</a>, <a href="http://tesaurus.kemdikbud.go.id/tematis/lema/mewadahi" class="lemma-ordinary">mewadahi</a></div></div></div><div class="result-postag"><i>verba</i></div><div class="result-set"><div class="article-label col-lg-2 col-md-2"><a href="http://tesaurus.kemdikbud.go.id/tematis/artikel/Peranti_Makan">PERANTI MAKAN</a></div><div class="one-par col-lg-9 col-md-9"><div class="one-par-content"><a href="http://tesaurus.kemdikbud.go.id/tematis/lema/menempatkan" class="lemma-ordinary">menempatkan</a>, <a href="http://tesaurus.kemdikbud.go.id/tematis/lema/menyajikan" class="lemma-ordinary">menyajikan</a>, <a href="http://tesaurus.kemdikbud.go.id/tematis/lema/menyimpan" class="lemma-ordinary">menyimpan</a>, <a href="http://tesaurus.kemdikbud.go.id/tematis/lema/mewadahi" class="lemma-ordinary">mewadahi</a></div></div></div></div>"""  # noqa: E501
SAMPLE_HTML_3 = """<div class="result-postag"><i>verba</i></div>"""


def test_lema_to_dict():
    sample = Lema("label", None, ["teks1", "teks2"])
    assert {"label": "label", "sublabel": None, "lema": ["teks1", "teks2"]} == sample.to_dict()


def test_tesaurus_sesi():
    sample = requests.Session()
    mock_header = {"Sample-Header": "Mocked"}
    sample.headers.update(mock_header)
    te = Tesaurus(sample)
    assert te.sesi.headers.get("Sample-Header") == "Mocked"


def test_tesaurus_sesi_close():
    te = Tesaurus()
    te.tutup()
    full_closed = True
    for adapter in te.sesi.adapters.values():
        if len(adapter.poolmanager.pools) > 0:
            full_closed = False
    assert full_closed is True


def test_tesaurusasync_sesi():
    sample = aiohttp.ClientSession(headers={"Sample-Header": "Mocked"})
    te = TesaurusAsync(sample)
    assert te.sesi.headers.get("Sample-Header") == "Mocked"


def test_tesaurusasync_sesi_cloes():
    loop = asyncio.get_event_loop()
    te = TesaurusAsync(loop=loop)
    loop.run_until_complete(te.tutup())
    assert te.sesi.closed is True


def test_tesaurus_buat_url():
    te = Tesaurus()
    te.kata = "mock"
    laman = te._buat_url()
    expect = f"{te.HOST}/mock"
    assert laman == expect


def test_tesaurus_buat_url_dengan_kelas():
    te = Tesaurus()
    te.kata = "mock"
    te.kelas_kata = "adjektiva"
    laman = te._buat_url()
    expect = f"{te.HOST}/mock/adjektiva"
    assert laman == expect


def test_tesaurus_buat_url_kelas_tidak_diketahui():
    te = Tesaurus()
    te.kata = "mock"
    te.kelas_kata = "adjective"
    with pytest.raises(KelasKataTidakDiketahui) as excinfo:
        te._buat_url()
    assert "Kelas kata adjective tidak diketahui." in str(excinfo.value)


def test_simulasi_404_error():
    te = Tesaurus()
    te.kata = "mock"
    sample = SimpleNamespace(status_code=404, text="")
    with pytest.raises(TidakDitemukan) as excinfo:
        te._cek_galat(sample)
    assert "Tidak dapat menemukan kata mock pada semua kelas kata" in str(excinfo)


def test_simulasi_404_error_dengan_kelas():
    te = Tesaurus()
    te.kata = "mock"
    te.kelas_kata = "adjektiva"
    sample = SimpleNamespace(status_code=404, text="")
    with pytest.raises(TidakDitemukan) as excinfo:
        te._cek_galat(sample)
    assert "Tidak dapat menemukan kata mock pada kelas kata adjektiva" in str(excinfo)


def test_simulasi_xxx_error():
    te = Tesaurus()
    te.kata = "mock"
    sample = SimpleNamespace(status_code=500, text="")
    with pytest.raises(TerjadiKesalahan) as excinfo:
        te._cek_galat(sample)
    assert "Terjadi kesalahan ketika berkomunikasi dengan website Tesaurus" in str(excinfo)


def test_simulasi_terkait_kosong():
    te = Tesaurus()
    te._buat_terkait("<div>mock</div>")
    assert te.terkait == []


def test_simulasi_terkait_error_silent():
    te = Tesaurus()
    te.kata = "makan"
    te._buat_terkait(SAMPLE_HTML_1)
    assert te.terkait == []


def test_simulasi_terkait_error_silent_2():
    te = Tesaurus()
    te.kata = "makan"
    te._buat_terkait(SAMPLE_HTML_2)
    assert len(te.terkait) == 1


def test_simulasi_str_tanpa_entri():
    te = Tesaurus()
    te.kata = "makan"
    assert "makan\nTidak ada hasil." == str(te)


def test_simulasi_lema_entri():
    lem = LemaEntri(SAMPLE_HTML_3)
    assert len(lem.entri) == 0


def test_simulasi_lema_entri_str():
    entri = LemaEntri(SAMPLE_HTML_3)
    assert "[verba]\nTidak ada entri" == str(entri)


def test_simulasi_lema_entri_repr():
    entri = LemaEntri(SAMPLE_HTML_3)
    assert "<LemaEntri: verba, 0 Entri>" == repr(entri)
