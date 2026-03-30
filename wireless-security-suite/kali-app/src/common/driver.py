import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from .utils import run_command


class DriverManager:
    def __init__(self, logger=None):
        self.logger = logger
        self.platform = "linux"

    def detect_adapters(self) -> list[dict]:
        adapters = []
        code, pci_out, _ = run_command(["lspci", "-nnk"])
        if code == 0:
            for line in pci_out.splitlines():
                if "Network controller" in line or "Ethernet controller" in line or "Bluetooth" in line:
                    adapters.append({"description": line.strip()})
        code, usb_out, _ = run_command(["lsusb"])
        if code == 0:
            for line in usb_out.splitlines():
                if any(keyword in line.lower() for keyword in ["bluetooth", "wireless", "network", "rfid", "lte", "gsm", "lorawan"]):
                    adapters.append({"description": line.strip()})
        return adapters

    def search_drivers(self) -> list[dict]:
        packages = []
        adapters = self.detect_adapters()
        for adapter in adapters:
            desc = adapter["description"].lower()
            if "rtl" in desc and "wifi" in desc:
                packages.append({"device": desc, "package": "rtl8188eu-dkms"})
            if "bluetooth" in desc:
                packages.append({"device": desc, "package": "bluez"})
            if "rtl" in desc and "sdr" in desc:
                packages.append({"device": desc, "package": "rtl-sdr"})
            if "nfc" in desc or "rfid" in desc:
                packages.append({"device": desc, "package": "libnfc-bin"})
        return packages

    def install_driver(self, package_name: str) -> dict:
        if not shutil.which("apt"):
            return {"error": "apt not found on this system"}
        code, stdout, stderr = run_command(["sudo", "apt", "install", "-y", package_name])
        return {"package": package_name, "returncode": code, "stdout": stdout, "stderr": stderr}

    def update_drivers(self) -> dict:
        if not shutil.which("apt"):
            return {"error": "apt not found on this system"}
        run_command(["sudo", "apt", "update"])
        returncode, stdout, stderr = run_command(["sudo", "apt", "upgrade", "-y"])
        return {"returncode": returncode, "stdout": stdout, "stderr": stderr}

    def save_driver_report(self, path: str = None) -> str:
        path = path or os.path.join(os.getcwd(), "driver-report.json")
        report = {"adapters": self.detect_adapters(), "candidates": self.search_drivers()}
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(report, handle, indent=2)
        return path
