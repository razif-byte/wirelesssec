from typing import List
from ..common.utils import run_command


class LoRaManager:
    def scan_lora(self) -> List[dict]:
        devices = []
        code, output, _ = run_command(["lsusb"])
        if code == 0:
            for line in output.splitlines():
                if "semtech" in line.lower() or "sx127x" in line.lower() or "lorawan" in line.lower():
                    devices.append({"device": line.strip()})
        if not devices:
            devices.append({"message": "No LoRa hardware found or drivers not installed"})
        return devices

    def report_frequency_usage(self) -> dict:
        return {"status": "placeholder", "message": "Real LoRa frequency monitoring requires a supported gateway or SDR."}
