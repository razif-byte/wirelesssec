from typing import List
try:
    from rtlsdr import RtlSdr
except ImportError:
    RtlSdr = None


class SDRManager:
    def list_supported_bands(self) -> List[dict]:
        return [
            {"band": "VLF", "range": "3-30 kHz"},
            {"band": "HF", "range": "3-30 MHz"},
            {"band": "VHF", "range": "30-300 MHz"},
            {"band": "UHF", "range": "300-3000 MHz"},
            {"band": "ADS-B", "range": "1090 MHz"},
        ]

    def list_devices(self) -> List[dict]:
        if RtlSdr is None:
            return [{"error": "pyrtlsdr not installed"}]
        try:
            devices = RtlSdr.get_device_count()
            return [{"index": idx, "device_count": devices} for idx in range(devices)]
        except Exception as exc:
            return [{"error": str(exc)}]

    def scan_band(self, frequency_mhz: float) -> dict:
        if RtlSdr is None:
            return {"error": "pyrtlsdr not installed"}
        try:
            with RtlSdr() as sdr:
                sdr.center_freq = frequency_mhz * 1e6
                sdr.sample_rate = 2.4e6
                sdr.gain = 'auto'
                return {"status": "started", "frequency_mhz": frequency_mhz}
        except Exception as exc:
            return {"error": str(exc)}
