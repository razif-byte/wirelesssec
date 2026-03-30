import json
import os
from datetime import datetime
from typing import List


class ChatManager:
    def __init__(self, storage_path: str = None):
        self.storage_path = storage_path or os.path.join(os.getcwd(), "chat-history.json")
        self._load_messages()

    def _load_messages(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, "r", encoding="utf-8") as handle:
                try:
                    self.messages = json.load(handle)
                except json.JSONDecodeError:
                    self.messages = []
        else:
            self.messages = []

    def _save_messages(self):
        with open(self.storage_path, "w", encoding="utf-8") as handle:
            json.dump(self.messages, handle, indent=2)

    def send_message(self, sender: str, text: str, channel: str = "local") -> dict:
        message = {
            "timestamp": datetime.utcnow().isoformat(),
            "sender": sender,
            "text": text,
            "channel": channel,
        }
        self.messages.append(message)
        self._save_messages()
        return message

    def get_messages(self, limit: int = 50) -> List[dict]:
        return self.messages[-limit:]
