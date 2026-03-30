import json
import os
import threading
import time
from datetime import datetime
from .utils import setup_logger


class AIMonitor:
    def __init__(self, logger=None):
        self.logger = logger or setup_logger("ai_monitor")
        self.health_log = []
        self.running = False

    def analyze_device_health(self, device_stats: dict) -> dict:
        score = 100
        issues = []
        battery = device_stats.get("battery", 100)
        security = device_stats.get("security", "good")
        power = device_stats.get("power_use", "normal")
        if battery < 30:
            issues.append("Low battery: optimize charging and lower power usage")
            score -= 20
        if security != "good":
            issues.append("Security warning: review network and Bluetooth settings")
            score -= 25
        if power == "high":
            issues.append("High power consumption detected: enable power saving")
            score -= 15
        return {"score": max(score, 0), "issues": issues, "timestamp": datetime.utcnow().isoformat()}

    def analyze_network(self, network_stats: dict) -> dict:
        issues = []
        if network_stats.get("unsecured_wifi"):
            issues.append("Unsecured WiFi detected")
        if network_stats.get("rogue_bluetooth"):
            issues.append("Unknown Bluetooth device found")
        return {"issues": issues, "summary": "Network analysis complete", "timestamp": datetime.utcnow().isoformat()}

    def monitor_loop(self, interval: int = 60):
        self.running = True
        self.logger.info("AI monitor started")
        while self.running:
            device_stats = {"battery": 75, "security": "good", "power_use": "normal"}
            summary = self.analyze_device_health(device_stats)
            self.health_log.append(summary)
            self.logger.info(f"AI monitor summary: {summary}")
            time.sleep(interval)

    def start(self, interval: int = 120):
        if not self.running:
            thread = threading.Thread(target=self.monitor_loop, args=(interval,), daemon=True)
            thread.start()
            return True
        return False

    def stop(self):
        self.running = False
        self.logger.info("AI monitor stopped")

    def report(self) -> dict:
        return {"health_checks": self.health_log[-10:]} if self.health_log else {"message": "No data yet"}
