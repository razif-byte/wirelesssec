from typing import List
from ..common.utils import run_command


class GSMManager:
    def scan_gsm(self) -> List[dict]:
        cells = []
        code, output, _ = run_command(["mmcli", "-L"])
        if code == 0:
            for line in output.splitlines():
                if "/Modem" in line:
                    cells.append({"modem": line.strip()})
        else:
            code, usb_out, _ = run_command(["lsusb"])
            for line in usb_out.splitlines():
                if any(keyword in line.lower() for keyword in ["qualcomm", "huawei", "sierra", "gsm", "lte"]):
                    cells.append({"device": line.strip()})
        return cells

    def get_modem_health(self) -> dict:
        return {"status": "placeholder", "message": "Modem health requires ModemManager and root privileges."}
