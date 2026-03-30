from typing import List
try:
    import nfc
except ImportError:
    nfc = None


class RFIDManager:
    def scan_tags(self) -> List[dict]:
        if nfc is None:
            return [{"error": "nfcpy package not installed"}]
        return [{"status": "waiting", "message": "RFID reader is available, scanning not yet implemented"}]

    def connect_reader(self) -> dict:
        return {"status": "placeholder", "message": "RFID reader connect requires hardware present."}
