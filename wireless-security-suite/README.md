# Wireless Security Suite

Projek ini adalah rangka kerja alat pemantauan dan kawalan frekuensi untuk Kali Linux dan aplikasi web mudah alih.
Ia menumpukan kepada:
- pengesanan dan sambungan WiFi termasuk pembacaan kata laluan tersimpan untuk rangkaian sendiri
- imbasan dan sambungan Bluetooth klasik dan BLE
- pengesanan modem GSM dan peranti LoRa
- sokongan asas SDR untuk UHF/VHF/ADS-B/VLF
- pemantauan RFID/NFC
- dashboard web Flask dengan login/signup
- sistem pemantauan AI untuk keselamatan dan kesihatan peranti
- pilihan audio / notifikasi suara dan sokongan push notifikasi mudah alih melalui Pushover
- sambungan host/client dengan sokongan QR code / IP / user ID / email / telefon
- skrip autorun untuk Linux dan Windows

## Cara Mula

1. Pasang kebergantungan:
   ```bash
   cd wireless-security-suite/kali-app
   python3 -m pip install -r requirements.txt
   ```
2. Mulakan dashboard:
   ```bash
   python3 app.py --serve
   ```
3. Buka `http://127.0.0.1:5000` dan daftar akaun baru.

## Deployment

- Static website akan dideploy ke GitHub Pages melalui GitHub Actions dari folder `webapp/`.
- Setelah workflow selesai, laman akan tersedia di `https://razif-byte.github.io/wirelesssec/`.
- Untuk aplikasi backend, `Procfile` dan `Dockerfile` telah disediakan untuk deployment ke platform percuma seperti Railway, Render, atau Heroku.

> Nota: alat ini direka untuk pemantauan dan pentadbiran yang sah sahaja. Jangan gunakan untuk mengganggu rangkaian atau peranti tanpa kebenaran.
