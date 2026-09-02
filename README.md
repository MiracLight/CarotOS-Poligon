# CarotOS Poligon

CarotOS Poligon, sızma testi araçlarının denetimli ve izole bir ortamda
öğretilmesi için hazırlanmış bir öğrenci/öğretmen uygulama çiftidir.
[CarotOS](https://github.com/MiracLight/CarotOS) dağıtımının bir parçası
olarak geliştirilmiştir ve dağıtımın ISO görüntüsüne dahildir.

## Genel Bakış

Öğretmen uygulaması bir sınıf odası açar ve bir oda kodu ile şifre üretir.
Öğrenciler bu bilgilerle kendi bilgisayarlarından odaya katılır ya da
öğretmenden bağımsız olarak bireysel modda pratik yapabilir. Her görev,
öğrencinin kendi makinesinde (127.0.0.1) çalışan sahte bir hedef üzerinde
çözülür; hiçbir görev ağ üzerinden gerçek bir sisteme erişim gerektirmez.

## Desteklenen Araçlar

| Araç | Kullanım Amacı |
|---|---|
| hydra | Kimlik doğrulama testi |
| nmap | Ağ ve port taraması |
| john | Parola gücü analizi |
| sqlmap | SQL enjeksiyon testi |
| tshark | Ağ trafiği çözümleme |
| ufw | Güvenlik duvarı yapılandırması (savunma görevi) |
| fail2ban | Saldırı engelleme (savunma görevi) |

## Gereksinimler

- Python 3.11 veya üzeri
- PyGObject (GTK 3)
- Yukarıdaki araçların sistemde kurulu olması (CarotOS ISO'sunda hazır gelir)

## Kullanım

```bash
# Öğretmen
python3 ogretmen_uygulama.py

# Öğrenci
python3 ogrenci_uygulama.py
```

Öğretmen uygulaması açılışta bir oda kodu ve şifre üretir; bu bilgiler
öğrencilerle paylaşılır. Öğrenci uygulaması açılışta bireysel pratik veya
sınıfa katılma seçeneği sunar.

## Mimari

- `ogretmen_sunucu.py` — öğretmen tarafında çalışan, `http.server` tabanlı
  basit bir HTTP sunucusu. Yalnızca `127.0.0.1` ve yerel ağ üzerinden
  erişilebilir; dışa açık bir servis değildir.
- `ogrenci_istemci.py` — öğrenci uygulamasının sunucuyla ve yerel sahte
  servislerle iletişimini yöneten istemci katmanı.
- `servisler/` — her görev için izole, minimal sahte hedef servisleri
  (gerçek bir sistemi taklit etmez, yalnızca ilgili aracın çalışabileceği
  bir hedef sunar).
- `gorevler/*.json` — görev tanımları: senaryo metni, doğru cevabın nasıl
  üretileceği, doğrulama yöntemi.
- `gorev_dogrulayici.py` — görev dosyalarının şemaya uygunluğunu denetleyen
  bağımsız bir araç.
- `gecmis_defteri.py` — bireysel modda ilerlemenin yerel olarak
  (`~/.local/share/carotos-poligon/`) saklanması.

## Güvenlik Notları

- Tüm sahte hedef servisler yalnızca `127.0.0.1` üzerinde dinler; bu kural
  şema doğrulayıcı tarafından da zorunlu kılınır.
- ufw/fail2ban görevleri öğrencinin kendi sudo yetkisini gerektirir;
  uygulama hiçbir zaman kendiliğinden yetki yükseltmez.
- Öğretmen paneline erişim, sistemin gerçek yönetici (sudo) parolasıyla
  doğrulanır.

## Testler

Depodaki `test_*.py` ile başlayan dosyalar, sunucu/istemci mantığını ve
GTK arayüzünü kapsayan testlerdir. Bazı testler ilgili araçların (hydra,
nmap vb.) sistemde kurulu olmasını gerektirir.

## Lisans

GNU General Public License v3.0. Ayrıntılar için `LICENSE` dosyasına
bakın.

## İlgili Depolar

- Dağıtım (ISO): https://github.com/MiracLight/CarotOS
- Web sitesi: https://carotos.org

---

# CarotOS Poligon (English)

CarotOS Poligon is a student/teacher application pair for teaching
penetration testing tools in a controlled, isolated environment. It is
developed as part of the [CarotOS](https://github.com/MiracLight/CarotOS)
distribution and ships with its ISO image.

## Overview

The teacher application opens a classroom room and generates a room code
and password. Students join the room from their own machines using this
information, or practice independently in individual mode. Every task is
solved against a fake target running on the student's own machine
(127.0.0.1); no task requires network access to a real system.

## Supported Tools

| Tool | Purpose |
|---|---|
| hydra | Authentication testing |
| nmap | Network and port scanning |
| john | Password strength analysis |
| sqlmap | SQL injection testing |
| tshark | Network traffic analysis |
| ufw | Firewall configuration (defense task) |
| fail2ban | Intrusion prevention (defense task) |

## Requirements

- Python 3.11 or later
- PyGObject (GTK 3)
- The tools listed above installed on the system (included by default on
  the CarotOS ISO)

## Usage

```bash
# Teacher
python3 ogretmen_uygulama.py

# Student
python3 ogrenci_uygulama.py
```

The teacher application generates a room code and password on startup,
which are shared with students. The student application offers a choice
between individual practice and joining a class.

## Architecture

- `ogretmen_sunucu.py` — a minimal HTTP server, based on `http.server`,
  running on the teacher's machine. Reachable only on `127.0.0.1` and the
  local network; it is not exposed publicly.
- `ogrenci_istemci.py` — the client layer handling communication between
  the student application, the server, and the local fake services.
- `servisler/` — isolated, minimal fake target services for each task
  (these do not emulate a real system; they only provide a target the
  relevant tool can operate against).
- `gorevler/*.json` — task definitions: scenario text, how the correct
  answer is generated, verification method.
- `gorev_dogrulayici.py` — a standalone tool that validates task files
  against the schema.
- `gecmis_defteri.py` — local storage of individual-mode progress
  (`~/.local/share/carotos-poligon/`).

## Security Notes

- All fake target services listen only on `127.0.0.1`; this rule is also
  enforced by the schema validator.
- The ufw/fail2ban tasks require the student's own sudo privileges; the
  application never escalates privileges on its own.
- Access to the teacher panel is verified against the system's real
  administrator (sudo) password.

## Tests

Files beginning with `test_*.py` cover the server/client logic and the
GTK interface. Some tests require the corresponding tools (hydra, nmap,
etc.) to be installed.

## License

GNU General Public License v3.0. See `LICENSE` for details.

## Related Repositories

- Distribution (ISO): https://github.com/MiracLight/CarotOS
- Website: https://carotos.org
