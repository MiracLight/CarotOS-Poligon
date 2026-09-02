"""
SINIF SEKMESI TESTI (yeni radyo düğmesi + Uygula davranışı):
- Görev seçimi radio button grubu, aynı anda sadece biri işaretli
- İşaretlemek HEMEN görevi açmaz, sadece seçimi belirler
- "Uygula" butonuna basınca işaretli olan görev açılır, diğerleri kapanır
"""

import sys
from pathlib import Path

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ogretmen_uygulama import OgretmenPenceresi  # noqa: E402


def main():
    pencere = OgretmenPenceresi()  # varsayılan hydra-01 açık başlar
    pencere.show_all()
    while Gtk.events_pending():
        Gtk.main_iteration()

    print("[TEST] Başlangıçta açık görevler:", pencere.oda.acik_gorevler)
    assert pencere.oda.acik_gorevler == {"hydra-01"}
    print("✓ Varsayılan olarak hydra-01 açık")

    hydra_radio = pencere._gorev_anahtarlari["hydra-01"]
    assert hydra_radio.get_active(), "hydra radio düğmesi UI'da işaretli görünmüyor"
    print("✓ hydra-01 radio düğmesi UI'da da işaretli")

    # --- Radio grubu: aynı anda sadece BİR düğme işaretli olabilmeli ---
    print("\n[TEST] nmap-01 radio düğmesini işaretliyoruz...")
    nmap_radio = pencere._gorev_anahtarlari["nmap-01"]
    nmap_radio.set_active(True)
    while Gtk.events_pending():
        Gtk.main_iteration()

    assert nmap_radio.get_active()
    assert not hydra_radio.get_active(), "radio grubu çalışmıyor, ikisi de işaretli"
    print("✓ nmap-01 işaretlenince hydra-01 otomatik işaretsiz oldu (radio davranışı)")

    # --- Sadece işaretlemek, sunucu tarafında HENÜZ görevi değiştirmemeli ---
    print(f"[TEST] İşaretledikten sonra, 'Uygula'ya basmadan önce sunucu durumu: {pencere.oda.acik_gorevler}")
    assert pencere.oda.acik_gorevler == {"hydra-01"}, \
        "işaretlemek hemen görevi açtı -- bu artık istenmeyen davranış"
    print("✓ İşaretlemek tek başına görevi DEĞİŞTİRMEDİ (beklenen davranış)")

    # --- "Uygula" butonuna basınca gerçek geçiş olmalı ---
    print("\n[TEST] 'Uygula' (Seçili Göreve Geç) butonuna basılıyor...")
    pencere.siradaki_dugmesi.clicked()
    while Gtk.events_pending():
        Gtk.main_iteration()
    print("Açık görevler:", pencere.oda.acik_gorevler)
    print("Durum etiketi:", pencere.sinif_durum_etiketi.get_text())
    assert pencere.oda.acik_gorevler == {"nmap-01"}, \
        f"beklenen nmap-01, gelen: {pencere.oda.acik_gorevler}"
    print("✓ 'Uygula' butonuna basınca işaretli olan görev (nmap-01) gerçekten açıldı")

    # --- Öğrencinin /gorevler ile bunu görmesi ---
    import urllib.request, json
    with urllib.request.urlopen("http://127.0.0.1:8642/gorevler") as r:
        cevap = json.loads(r.read())
    print(f"\n[ÖĞRENCİ] /gorevler cevabı: {cevap}")
    assert cevap["acik_gorevler"] == ["nmap-01"]
    print("✓ Öğrenci tarafı da artık nmap-01'in açık olduğunu görüyor")

    # --- Farklı bir görevi seçip tekrar Uygula'ya basma ---
    print("\n[TEST] tshark-01'i işaretleyip tekrar Uygula'ya basılıyor...")
    pencere._gorev_anahtarlari["tshark-01"].set_active(True)
    pencere.siradaki_dugmesi.clicked()
    while Gtk.events_pending():
        Gtk.main_iteration()
    assert pencere.oda.acik_gorevler == {"tshark-01"}
    print("✓ İstenilen HERHANGİ bir göreve (sıra gözetmeksizin) geçilebiliyor")

    pencere.sunucu.shutdown()
    print("\n" + "=" * 70)
    print("✓ SINIF SEKMESİ (RADIO + UYGULA DAVRANIŞI) TAM ÇALIŞIYOR")
    print("=" * 70)


if __name__ == "__main__":
    main()
