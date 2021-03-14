import os

from tesaurus import TidakDitemukan

from _mock import MockTesaurus, MockTesaurusAsync

_KASUS_PATH = os.path.join(os.getcwd(), "tests", "kasus")


def read_kasus(nama, kelas=None):
    path = nama
    if kelas:
        path += f"_{kelas}"
    path += ".txt"
    with open(os.path.join(_KASUS_PATH, path), "r", encoding="utf-8") as fp:
        return fp.read()


def test_tanpa_kelas_kata():
    kasus = str(read_kasus("makan")).rstrip("\n")
    te = MockTesaurus()
    te.cari("makan")
    res = str(te).rstrip("\n")
    assert res == kasus


def test_dengan_kelas_kata():
    kasus = str(read_kasus("makan", "adjektiva")).rstrip("\n")
    te = MockTesaurus()
    te.cari("makan", "adjektiva")
    res = str(te).rstrip("\n")
    assert res == kasus


def test_kata_tidak_ditemukan():
    te = MockTesaurus()
    err_txt = ""
    try:
        te.cari("katatidakvalid")
    except TidakDitemukan as errmsg:
        err_txt = str(errmsg)
    assert err_txt == "Tidak dapat menemukan kata katatidakvalid pada semua kelas kata."


def test_kata_tidak_ditemukan_dengan_kelas_kata():
    te = MockTesaurus()
    err_txt = ""
    try:
        te.cari("katatidakvalid", "konjungsi")
    except TidakDitemukan as errmsg:
        err_txt = str(errmsg)
    assert err_txt == "Tidak dapat menemukan kata katatidakvalid pada kelas kata konjungsi."