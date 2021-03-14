import argparse
import json
import sys
import traceback

from .tesaurus import (
    KelasKataTidakDiketahui,
    TerjadiKesalahan,
    Tesaurus,
    TesaurusGalat,
    TidakDitemukan,
    __author__,
    __version__,
)


def cli():
    parser = argparse.ArgumentParser(
        prog="tesaurus", description="Mencari informasi tesaurus dari Tesaurus Tematis", add_help=False
    )
    parser.add_argument("kata", help="Kata atau kalimat yang ingin dicari")
    parser.add_argument(
        "-h",
        "-b",
        "--help",
        "--bantuan",
        action="help",
        help="tampilkan pesan bantuan ini dan keluar",
    )
    parser.add_argument(
        "-V",
        "--versi",
        "--version",
        action="version",
        help="Melihat versi Tesaurus dan keluar",
        version=f"tesaurus-python versi {__version__}, dibuat oleh {__author__}",
    )
    parser.add_argument(
        "-t",
        "---dengan-terkait",
        help="Tampilkan hasil terkait (bila ada)",
        action="store_true",
        dest="terkait",
    )
    parser.add_argument(
        "-k",
        "--kelas-kata",
        help="Batasi hasil ke kelas kata tertentu",
        default=None,
        choices=["adjektiva", "adverbia", "konjungsi", "nomina", "numeralia", "partikel", "verba"],
        dest="kelas",
    )
    parser.add_argument("-j", "--json", help="Tampilkan hasil dengan format JSON", action="store_true")
    parser.add_argument(
        "-i", "--indentasi", help="gunakan identasi sebanyak N untuk format JSON", type=int, metavar="N"
    )
    args = parser.parse_args()

    te = Tesaurus()
    try:
        te.cari(args.kata, args.kelas)
    except KelasKataTidakDiketahui:
        print(f"Kelas kata {args.kelas} tidak diketahui.")
        te.tutup()
        sys.exit(1)
    except TidakDitemukan:
        hasil = f"Tidak dapat menemukan kata {args.kata}"
        if args.kelas:
            hasil += f" di kelas kata {args.kelas}"
        print(hasil + ".")
        te.tutup()
        sys.exit(1)
    except TerjadiKesalahan:
        print("Terjadi kesalahan ketika ingin berkomunikasi dengan Tesaurus Tematis")
        te.tutup()
        sys.exit(1)
    except TesaurusGalat as ertg:
        tb = traceback.format_exception(type(ertg), ertg, ertg.__traceback__)
        print("Terjadi kesalahan internal, mohon kontak developer.")
        print("".join(tb))
        te.tutup()
        sys.exit(1)

    te.tutup()

    try:
        if args.json:
            print(json.dumps(te.serialisasi(), indent=args.indentasi))
        else:
            print(te.__str__(args.terkait))
    except TesaurusGalat as ertg:
        tb = traceback.format_exception(type(ertg), ertg, ertg.__traceback__)
        print("Terjadi kesalahan internal, mohon kontak developer.")
        print("".join(tb))
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    cli()
