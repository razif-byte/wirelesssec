# Usage

## Jalankan Web Dashboard

1. Pasang kebergantungan:
   ```bash
   cd wireless-security-suite/kali-app
   python3 -m pip install -r requirements.txt
   ```
2. Mula aplikasi:
   ```bash
   python3 app.py --serve
   ```
3. Akses papan pemuka di `http://127.0.0.1:5000`.

## Pilihan CLI

- `--scan-wifi`: imbas rangkaian WiFi tersedia.
- `--scan-bluetooth`: imbas peranti Bluetooth.
- `--scan-ble`: imbas peranti BLE.
- `--scan-sdr`: papar jalur SDR sokongan.
- `--scan-gsm`: imbas peranti GSM / modem.
- `--scan-lora`: imbas peranti LoRa.
- `--scan-rfid`: imbas tag RFID.

## Autorun

- `kali-app/scripts/autorun.sh` untuk Linux.
- `kali-app/scripts/autorun.bat` untuk Windows.
