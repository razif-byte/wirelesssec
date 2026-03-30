from typing import List
import asyncio
try:
    from bleak import BleakScanner
except ImportError:
    BleakScanner = None


class BLEManager:
    def scan_devices(self, timeout: int = 5) -> List[dict]:
        if BleakScanner is None:
            return [{"error": "bleak package not installed"}]
        devices = []
        found = asyncio.run(BleakScanner.discover(timeout=timeout))
        for device in found:
            devices.append({"address": device.address, "name": device.name, "rssi": device.rssi})
        return devices

    def connect(self, address: str) -> dict:
        return {"status": "placeholder", "address": address, "message": "BLE connect function is available after pairing workflow."}
