import subprocess
from typing import List
from ..common.utils import run_command


class BluetoothManager:
    def scan_devices(self) -> List[dict]:
        devices = []
        code, output, _ = run_command(["bluetoothctl", "devices"])
        if code == 0:
            for line in output.splitlines():
                if line.startswith("Device"):
                    parts = line.split(" ", 2)
                    if len(parts) >= 3:
                        devices.append({"mac": parts[1], "name": parts[2]})
        return devices

    def pair_device(self, mac_address: str) -> dict:
        code, stdout, stderr = run_command(["bluetoothctl", "pair", mac_address])
        return {"mac": mac_address, "returncode": code, "stdout": stdout, "stderr": stderr}

    def connect(self, mac_address: str) -> dict:
        code, stdout, stderr = run_command(["bluetoothctl", "connect", mac_address])
        return {"mac": mac_address, "returncode": code, "stdout": stdout, "stderr": stderr}
