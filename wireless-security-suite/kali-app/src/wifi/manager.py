import os
import json
from pathlib import Path
from typing import List
from ..common.utils import run_command


class WiFiManager:
    def __init__(self):
        self.platform = "linux"

    def scan_wifi(self) -> List[dict]:
        networks = []
        code, output, error = run_command(["nmcli", "-f", "SSID,BSSID,SIGNAL,SECURITY", "device", "wifi", "list"])
        if code == 0:
            for line in output.splitlines()[1:]:
                parts = [part.strip() for part in line.split("  ") if part.strip()]
                if parts:
                    networks.append({"raw": line.strip(), "fields": parts})
        return networks

    def connect(self, ssid: str, password: str = None) -> dict:
        if password:
            code, stdout, stderr = run_command(["nmcli", "device", "wifi", "connect", ssid, "password", password])
        else:
            code, stdout, stderr = run_command(["nmcli", "device", "wifi", "connect", ssid])
        return {"ssid": ssid, "returncode": code, "stdout": stdout, "stderr": stderr}

    def get_saved_passwords(self) -> List[dict]:
        results = []
        config_path = Path("/etc/NetworkManager/system-connections")
        if not config_path.exists():
            return results
        for profile in config_path.glob("*"):
            try:
                content = profile.read_text(encoding="utf-8", errors="ignore")
                if "psk=" in content:
                    result = {"profile": profile.name, "ssid": None, "password": None}
                    for line in content.splitlines():
                        if line.startswith("ssid="):
                            result["ssid"] = line.split("=", 1)[1]
                        if line.startswith("psk="):
                            result["password"] = line.split("=", 1)[1]
                    results.append(result)
            except PermissionError:
                continue
        return results

    def find_password(self, ssid: str) -> dict:
        for profile in self.get_saved_passwords():
            if profile.get("ssid") == ssid:
                return profile
        return {"ssid": ssid, "password": None, "error": "SSID not found in saved profiles"}
