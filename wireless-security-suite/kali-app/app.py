import argparse
import logging
import os
from src.dashboard.api import create_dashboard
from src.common.utils import setup_logger
from src.wifi.manager import WiFiManager
from src.bluetooth.manager import BluetoothManager
from src.ble.manager import BLEManager
from src.sdr.manager import SDRManager
from src.gsm.manager import GSMManager
from src.lora.manager import LoRaManager
from src.rfid.manager import RFIDManager

logger = setup_logger("wireless_security_suite")


def main():
    parser = argparse.ArgumentParser(description="Wireless Security Suite")
    parser.add_argument("--serve", action="store_true", help="Start the dashboard web server")
    parser.add_argument("--scan-wifi", action="store_true", help="Scan for nearby WiFi networks")
    parser.add_argument("--scan-bluetooth", action="store_true", help="Scan for Bluetooth devices")
    parser.add_argument("--scan-ble", action="store_true", help="Scan for BLE devices")
    parser.add_argument("--scan-sdr", action="store_true", help="Scan SDR bands")
    parser.add_argument("--scan-gsm", action="store_true", help="Detect GSM cells")
    parser.add_argument("--scan-lora", action="store_true", help="Scan LoRa frequencies")
    parser.add_argument("--scan-rfid", action="store_true", help="Scan RFID/NFC")
    parser.add_argument("--ai-monitor", action="store_true", help="Run the AI monitoring engine")
    parser.add_argument("--auto-driver", action="store_true", help="Search and install missing drivers automatically")
    parser.add_argument("--start-host", action="store_true", help="Start a local connection host server")
    parser.add_argument("--join-client", nargs=2, metavar=("IP", "PORT"), help="Join a remote host as client")
    parser.add_argument("--qrcode", action="store_true", help="Generate connection QR code payload")
    args = parser.parse_args()

    if args.serve:
        app = create_dashboard()
        app.run(host="0.0.0.0", port=5000, debug=False)
        return

    if args.scan_wifi:
        manager = WiFiManager()
        networks = manager.scan_wifi()
        logger.info(f"Found {len(networks)} WiFi networks")
        for item in networks:
            print(item)

    if args.scan_bluetooth:
        manager = BluetoothManager()
        devices = manager.scan_devices()
        logger.info(f"Found {len(devices)} Bluetooth devices")
        for entry in devices:
            print(entry)

    if args.scan_ble:
        manager = BLEManager()
        devices = manager.scan_devices()
        logger.info(f"Found {len(devices)} BLE devices")
        for item in devices:
            print(item)

    if args.scan_sdr:
        manager = SDRManager()
        bands = manager.list_supported_bands()
        logger.info("SDR supported bands:")
        for band in bands:
            print(band)

    if args.scan_gsm:
        manager = GSMManager()
        cells = manager.scan_gsm()
        logger.info(f"Found {len(cells)} GSM cells")
        for cell in cells:
            print(cell)

    if args.scan_lora:
        manager = LoRaManager()
        anchors = manager.scan_lora()
        logger.info(f"Found {len(anchors)} LoRa signals")
        for anchor in anchors:
            print(anchor)

    if args.scan_rfid:
        manager = RFIDManager()
        tags = manager.scan_tags()
        logger.info(f"Found {len(tags)} RFID tags")
        for tag in tags:
            print(tag)

    if args.ai_monitor:
        from src.common.monitor import AIMonitor
        monitor = AIMonitor()
        monitor.start(interval=10)
        logger.info("AI monitoring started in background")

    if args.auto_driver:
        from src.common.driver import DriverManager
        driver = DriverManager()
        candidates = driver.search_drivers()
        logger.info(f"Found {len(candidates)} candidate drivers")
        for candidate in candidates:
            print(candidate)
            result = driver.install_driver(candidate["package"])
            print(result)

    if args.start_host:
        from src.common.connection import ConnectionManager
        conn = ConnectionManager()
        print(conn.start_host())

    if args.join_client:
        from src.common.connection import ConnectionManager
        target_ip, target_port = args.join_client
        conn = ConnectionManager()
        print(conn.join_client(target_ip, int(target_port)))

    if args.qrcode:
        from src.common.connection import ConnectionManager
        conn = ConnectionManager()
        print(conn.get_qr_payload())


if __name__ == "__main__":
    main()
