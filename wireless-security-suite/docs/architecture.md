# Architecture

Projek Wireless Security Suite dibahagikan kepada beberapa modul:

- `kali-app/src/wifi`: pengurusan WiFi, imbasan, sambungan dan pembacaan kata laluan tersimpan.
- `kali-app/src/bluetooth`: imbasan dan sambungan Bluetooth klasik.
- `kali-app/src/ble`: imbasan BLE dan kawalan peranti.
- `kali-app/src/gsm`: pencarian peranti GSM / modem.
- `kali-app/src/lora`: pengesanan peranti LoRa.
- `kali-app/src/sdr`: sokongan untuk SDR dan imbasan frekuensi.
- `kali-app/src/rfid`: sokongan RFID/NFC.
- `kali-app/src/common`: utiliti umum, pengurusan pemandu, sistem pemantauan AI, kawalan sambungan dan chat.
- `kali-app/src/dashboard`: aplikasi web Flask dengan login/signup, papan pemuka, chat, notifikasi dan connection host/client.
