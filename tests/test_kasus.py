import asyncio
import json
import os

import pytest
from tesaurus import Tesaurus, TesaurusGalat, TidakDitemukan

from _mock import MockTesaurus, MockTesaurusAsync

_KASUS_PATH = os.path.join(os.getcwd(), "tests", "kasus")
_SERIALISAS_PATH = os.path.join(os.getcwd(), "tests", "serialisasi")


def read_kasus(nama, kelas=None, terkait=False):
    path = nama
    if kelas:
        path += f"_{kelas}"
    if terkait:
        path += "_terkait"
    path += ".txt"
    with open(os.path.join(_KASUS_PATH, path), "r", encoding="utf-8") as fp:
        return fp.read()


def read_serialisasi(nama, kelas=None):
    path = nama
    if kelas:
        path += f"_{kelas}"
    path += ".json"
    with open(os.path.join(_SERIALISAS_PATH, path), "r", encoding="utf-8") as fp:
        return json.load(fp)


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


def test_kata_cache():
    kasus = str(read_kasus("makan")).rstrip("\n")
    te = MockTesaurus()
    te.cari("makan")
    res_old = str(te).rstrip("\n")
    te.cari("makan")
    res_new = str(te).rstrip("\n")
    assert res_old == kasus and res_new == res_old


def test_async_tanpa_kelas_kata():
    kasus = str(read_kasus("makan")).rstrip("\n")
    te = MockTesaurusAsync()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(te.cari("makan"))
    res = str(te).rstrip("\n")
    assert res == kasus


def test_async_dengan_kelas_kata():
    kasus = str(read_kasus("makan", "adjektiva")).rstrip("\n")
    te = MockTesaurusAsync()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(te.cari("makan", "adjektiva"))
    res = str(te).rstrip("\n")
    assert res == kasus


def test_async_kata_cache():
    kasus = str(read_kasus("makan")).rstrip("\n")
    te = MockTesaurusAsync()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(te.cari("makan"))
    res_old = str(te).rstrip("\n")
    loop.run_until_complete(te.cari("makan"))
    res_new = str(te).rstrip("\n")
    assert res_old == kasus and res_new == res_old


def test_kata_dengan_terkait():
    kasus = str(read_kasus("makan", None, True)).rstrip("\n")
    te = MockTesaurus()
    te.cari("makan")
    res = te.__str__(terkait=True).rstrip("\n")
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


def test_kata_serialisasi():
    kasus = read_serialisasi("makan")
    te = MockTesaurus()
    te.cari("makan")
    serialized = te.serialisasi()
    pranala = serialized["pranala"]
    pranala = pranala.replace("http://localhost:4000/", "https://tesaurus.kemdikbud.go.id/tematis/lema/")
    pranala = pranala.replace(".html", "")
    serialized["pranala"] = pranala
    assert serialized == kasus


def test_kata_repr():
    te = MockTesaurus()
    te.cari("makan")
    assert "<Tesaurus: makan>" == repr(te)


def test_kata_repr_dengan_kelas():
    te = MockTesaurus()
    te.cari("makan", "adjektiva")
    assert "<Tesaurus: makan [adjektiva]>" == repr(te)


def test_tidak_ada_kata_repr():
    te = MockTesaurus()
    assert "<Tesaurus: TidakAda>" == repr(te)


def test_kata_repr_async():
    te = MockTesaurusAsync()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(te.cari("makan"))
    loop.run_until_complete(te.tutup())
    assert "<TesaurusAsync: makan>" == repr(te)


def test_kata_repr_dengan_kelas_async():
    te = MockTesaurusAsync()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(te.cari("makan", "adjektiva"))
    loop.run_until_complete(te.tutup())
    assert "<TesaurusAsync: makan [adjektiva]>" == repr(te)


def test_tidak_ada_kata_repr_async():
    te = MockTesaurusAsync()
    assert "<TesaurusAsync: TidakAda>" == repr(te)


def test_tesaurus_entri():
    te = Tesaurus()
    assert te.entri == []


def test_tesaurus_terkait():
    te = Tesaurus()
    assert te.terkait == []


def test_tidak_ada_kata():
    te = MockTesaurus()
    assert "Tidak ada kata yang sedang dicari" in str(te)


def test_tidak_ada_kata_serialisasi():
    te = MockTesaurus()
    with pytest.raises(TesaurusGalat) as excinfo:
        te.serialisasi()
    assert "Tidak ada kata yang sedang dicari" in str(excinfo.value)
