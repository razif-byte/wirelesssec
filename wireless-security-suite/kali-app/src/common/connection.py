import json
import socket
import threading
from typing import Optional


class ConnectionManager:
    def __init__(self, host: str = "0.0.0.0", port: int = 9000):
        self.host = host
        self.port = port
        self.server_socket: Optional[socket.socket] = None
        self.client_sockets = []
        self.server_thread: Optional[threading.Thread] = None
        self.running = False

    def _serve(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(4)
        self.running = True
        while self.running:
            client, address = self.server_socket.accept()
            self.client_sockets.append(client)
            client.sendall(b"WELCOME|connected")

    def start_host(self) -> dict:
        if self.running:
            return {"status": "already_running"}
        self.server_thread = threading.Thread(target=self._serve, daemon=True)
        self.server_thread.start()
        return {"status": "host_started", "host": self.host, "port": self.port}

    def join_client(self, target_ip: str, target_port: int = 9000, identity: str = None) -> dict:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target_ip, target_port))
            payload = json.dumps({"identity": identity or "anonymous"}).encode("utf-8")
            sock.sendall(payload)
            data = sock.recv(1024).decode("utf-8", errors="ignore")
            sock.close()
            return {"status": "connected", "remote_response": data}
        except Exception as exc:
            return {"status": "error", "message": str(exc)}

    def get_qr_payload(self, user_id: str = None, email: str = None, phone: str = None) -> dict:
        return {"host": self.host, "port": self.port, "user_id": user_id, "email": email, "phone": phone}

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        for client in self.client_sockets:
            client.close()
        self.client_sockets = []
        return {"status": "stopped"}
