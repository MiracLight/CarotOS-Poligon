"""
Öğretmen 'Sıradaki Göreve Geç' derken, ZATEN GTK penceresi açık olan
öğrencinin ekranının GERÇEKTEN otomatik güncellendiğini test eder.
"""

import sys
import time
from pathlib import Path

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ogretmen_uygulama import OgretmenPenceresi  # noqa: E402
from ogrenci_uygulama import PoligonPenceresi  # noqa: E402


def main():
    ogretmen = OgretmenPenceresi(gorev_id="hydra-01")
    ogretmen.show_all()
    while Gtk.events_pending():
        Gtk.main_iteration()

    ogrenci_pencere = PoligonPenceresi()
    ogrenci_pencere.show_all()
    while Gtk.events_pending():
        Gtk.main_iteration()

    # Öğrenci sınıfa katılıyor
    ogrenci_pencere.sinif_mod_dugmesi.clicked()
    while Gtk.events_pending():
        Gtk.main_iteration()
    ogrenci_pencere.kod_girisi.set_text(ogretmen.oda.oda_kodu)
    ogrenci_pencere.sifre_girisi.set_text(ogretmen.oda.sifre)
    ogrenci_pencere.ad_girisi.set_text("test_ogr")
    ogrenci_pencere.katil_dugmesi.clicked()

    for _ in range(20):
        time.sleep(0.1)
        while Gtk.events_pending():
            Gtk.main_iteration()

    print(f"[ÖĞRENCİ] Katıldı, görev: {ogrenci_pencere.gorev_verisi['id']}")
    assert ogrenci_pencere.gorev_verisi["id"] == "hydra-01"

    print("\n[ÖĞRETMEN] john-01'i seçip 'Uygula'ya basıyor (öğrenci penceresi AÇIK, hiçbir şey yapmıyor)...")
    ogretmen._gorev_anahtarlari["john-01"].set_active(True)
    ogretmen.siradaki_dugmesi.clicked()
    while Gtk.events_pending():
        Gtk.main_iteration()
    print(f"[ÖĞRETMEN] Sunucuda açık görev: {ogretmen.oda.acik_gorevler}")

    print("\n[TEST] Öğrenci izleme döngüsünün çalışması için 4 saniye bekleniyor...")
    for _ in range(45):  # ~4.5 saniye, izleme döngüsü 3 sn'de bir çalışıyor
        time.sleep(0.1)
        while Gtk.events_pending():
            Gtk.main_iteration()

    print(f"[ÖĞRENCİ] Ekrandaki görev ŞİMDİ: {ogrenci_pencere.gorev_verisi['id']}")
    assert ogrenci_pencere.gorev_verisi["id"] == "john-01", \
        f"öğrenci ekranı hâlâ eski görevde: {ogrenci_pencere.gorev_verisi['id']}"
    print("✓ Öğrenci penceresi HİÇBİR ŞEY YAPMADAN otomatik olarak yeni göreve geçti")

    # Sohbet günlüğünde bildirim var mı?
    notlar = [m["metin"] for m in ogrenci_pencere._sohbet_mesajlari]
    print(f"[ÖĞRENCİ] Not günlüğü: {notlar}")
    assert any("yeni bir göreve geçti" in n for n in notlar)
    print("✓ Öğrenciye görev değişikliği bildirimi de düştü")

    # Yeni görevi gerçekten çözebiliyor mu?
    dogru_cevap = ogrenci_pencere.istemci._dogru_cevap
    ogrenci_pencere.cevap_girisi.set_text(str(dogru_cevap))
    ogrenci_pencere.gonder_dugmesi.clicked()
    while Gtk.events_pending():
        Gtk.main_iteration()
    sonuc = ogrenci_pencere.sonuc_etiketi.get_text()
    print(f"[ÖĞRENCİ] Yeni görevi çözme sonucu: {sonuc}")
    assert "✓" in sonuc or "Doğru" in sonuc
    print("✓ Otomatik geçilen yeni görev gerçekten çözülebiliyor")

    ogrenci_pencere.istemci.gorevi_durdur()
    ogretmen.sunucu.shutdown()

    print("\n" + "=" * 70)
    print("✓ OTOMATİK GÖREV GEÇİŞİ GTK'DA UÇTAN UCA ÇALIŞIYOR")
    print("=" * 70)


if __name__ == "__main__":
    main()
