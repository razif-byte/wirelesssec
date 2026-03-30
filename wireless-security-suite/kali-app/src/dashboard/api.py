import json
import os
import shutil
import subprocess
from flask import Flask, render_template, redirect, url_for, request, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..wifi.manager import WiFiManager
from ..bluetooth.manager import BluetoothManager
from ..ble.manager import BLEManager
from ..sdr.manager import SDRManager
from ..gsm.manager import GSMManager
from ..lora.manager import LoRaManager
from ..rfid.manager import RFIDManager
from ..common.driver import DriverManager
from ..common.monitor import AIMonitor
from ..common.connection import ConnectionManager
from ..common.chat import ChatManager

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
USER_STORE = os.path.join(BASE_DIR, "config", "users.json")


def ensure_user_store():
    store_dir = os.path.dirname(USER_STORE)
    if not os.path.exists(store_dir):
        os.makedirs(store_dir, exist_ok=True)
    if not os.path.exists(USER_STORE):
        with open(USER_STORE, "w", encoding="utf-8") as handle:
            json.dump({"users": []}, handle)


def load_users():
    ensure_user_store()
    with open(USER_STORE, "r", encoding="utf-8") as handle:
        return json.load(handle)


def save_users(data):
    ensure_user_store()
    with open(USER_STORE, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def create_dashboard():
    app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"), static_folder=os.path.join(os.path.dirname(__file__), "static"))
    app.secret_key = os.environ.get("SECRET_KEY", "wireless-suite-secret")
    monitor = AIMonitor()
    monitor.start(interval=120)
    driver_manager = DriverManager()
    wifi_manager = WiFiManager()
    bt_manager = BluetoothManager()
    ble_manager = BLEManager()
    sdr_manager = SDRManager()
    gsm_manager = GSMManager()
    lora_manager = LoRaManager()
    rfid_manager = RFIDManager()
    connection_manager = ConnectionManager()
    chat_manager = ChatManager(storage_path=os.path.join(BASE_DIR, "kali-app", "config", "chat-history.json"))

    def current_user():
        return session.get("user")

    @app.route("/")
    def root():
        if session.get("user"):
            return redirect(url_for("dashboard"))
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            data = load_users()
            email = request.form.get("email")
            password = request.form.get("password")
            for user in data.get("users", []):
                if user["email"] == email and check_password_hash(user["password"], password):
                    session["user"] = {"email": email, "name": user.get("name", email)}
                    return redirect(url_for("dashboard"))
            flash("Invalid credentials", "danger")
        return render_template("login.html")

    @app.route("/signup", methods=["GET", "POST"])
    def signup():
        if request.method == "POST":
            data = load_users()
            email = request.form.get("email")
            password = request.form.get("password")
            name = request.form.get("name")
            if any(user["email"] == email for user in data.get("users", [])):
                flash("Email already registered", "warning")
                return render_template("signup.html")
            data["users"].append({"email": email, "name": name, "password": generate_password_hash(password)})
            save_users(data)
            flash("Signup berhasil, sila login", "success")
            return redirect(url_for("login"))
        return render_template("signup.html")

    @app.route("/logout")
    def logout():
        session.pop("user", None)
        return redirect(url_for("login"))

    @app.route("/dashboard")
    def dashboard():
        if not current_user():
            return redirect(url_for("login"))
        return render_template("dashboard.html", user=current_user())

    @app.route("/api/scan/<module>")
    def scan_module(module):
        if not current_user():
            return jsonify({"error": "authentication required"}), 401
        module = module.lower()
        if module == "wifi":
            return jsonify(wifi_manager.scan_wifi())
        if module == "bluetooth":
            return jsonify(bt_manager.scan_devices())
        if module == "ble":
            return jsonify(ble_manager.scan_devices())
        if module == "sdr":
            return jsonify(sdr_manager.list_supported_bands())
        if module == "gsm":
            return jsonify(gsm_manager.scan_gsm())
        if module == "lora":
            return jsonify(lora_manager.scan_lora())
        if module == "rfid":
            return jsonify(rfid_manager.scan_tags())
        return jsonify({"error": "unknown module"}), 404

    @app.route("/api/driver/search")
    def api_driver_search():
        return jsonify(driver_manager.search_drivers())

    @app.route("/api/driver/install", methods=["POST"])
    def api_driver_install():
        package = request.json.get("package")
        return jsonify(driver_manager.install_driver(package))

    @app.route("/api/driver/update", methods=["POST"])
    def api_driver_update():
        return jsonify(driver_manager.update_drivers())

    @app.route("/api/ai/status")
    def api_ai_status():
        return jsonify(monitor.report())

    @app.route("/api/notify", methods=["POST"])
    def api_notify():
        payload = request.json or {}
        message = payload.get("message", "Notification dari Wireless Security Suite")
        urgency = payload.get("urgency", "normal")
        _play_notification(message)
        _push_mobile_notification(message, payload.get("service"))
        return jsonify({"status": "sent", "message": message, "urgency": urgency})

    @app.route("/api/chat/send", methods=["POST"])
    def api_chat_send():
        payload = request.json or {}
        sender = current_user().get("name", "anonymous") if current_user() else "anonymous"
        msg = chat_manager.send_message(sender, payload.get("text", ""), payload.get("channel", "local"))
        return jsonify(msg)

    @app.route("/api/chat/messages")
    def api_chat_messages():
        return jsonify(chat_manager.get_messages())

    @app.route("/api/connection/host", methods=["POST"])
    def api_connection_host():
        return jsonify(connection_manager.start_host())

    @app.route("/api/connection/join", methods=["POST"])
    def api_connection_join():
        payload = request.json or {}
        ip = payload.get("ip")
        port = int(payload.get("port", 9000))
        identity = payload.get("identity")
        return jsonify(connection_manager.join_client(ip, port, identity))

    @app.route("/api/connection/qrcode")
    def api_connection_qrcode():
        payload = connection_manager.get_qr_payload(
            user_id=request.args.get("user_id"), email=request.args.get("email"), phone=request.args.get("phone")
        )
        return jsonify(payload)

    @app.route("/api/update-ui", methods=["POST"])
    def api_update_ui():
        return jsonify({"status": "ui_update_requested", "theme": request.json.get("theme", "default")})

    def _play_notification(message: str):
        if shutil.which("spd-say"):
            subprocess.Popen(["spd-say", message])
        elif shutil.which("espeak"):
            subprocess.Popen(["espeak", message])

    def _push_mobile_notification(message: str, service: str = None):
        # Optional integration with Pushover or webhook service if configured
        if service == "pushover":
            token = os.environ.get("PUSHOVER_TOKEN")
            user = os.environ.get("PUSHOVER_USER")
            if token and user:
                subprocess.run(["curl", "-s", "-F", f"token={token}", "-F", f"user={user}", "-F", f"message={message}", "https://api.pushover.net/1/messages.json"])

    return app
