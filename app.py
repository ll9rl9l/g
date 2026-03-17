from flask import Flask, render_template
from config import Config
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
import random
import datetime
import os  # ✅ مهم للPORT

# =======================
# Flask App Configuration
# =======================
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)

# =======================
# Encryption Setup
# =======================
cipher = Fernet(Config.ENCRYPTION_KEY)

def encrypt_text(text):
    return cipher.encrypt(text.encode())

def decrypt_text(enc_text):
    return cipher.decrypt(enc_text).decode()

# =======================
# Database Model
# =======================
class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(50))
    event_type = db.Column(db.String(100))
    description = db.Column(db.LargeBinary)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# =======================
# IDS Functions
# =======================
def add_ids_event(ip, event_type, description):
    log = Log(
        ip_address=ip,
        event_type=event_type,
        description=encrypt_text(description)
    )
    db.session.add(log)
    db.session.commit()
    print(f"[ALERT] {ip} | {event_type} | {description}")

def simulate_attack():
    events = [
        ("Port Scan","Multiple ports scanned"),
        ("Brute Force","Multiple login failures detected"),
        ("Malware Activity","Suspicious file execution detected")
    ]
    ip = f"192.168.1.{random.randint(1,254)}"
    event = random.choice(events)
    add_ids_event(ip,event[0],event[1])

def generate_fake_logs(count=200):
    events = [
        ("Port Scan","Multiple ports scanned"),
        ("Brute Force","Multiple login failures detected"),
        ("Malware Activity","Suspicious file execution detected")
    ]
    for i in range(count):
        ip = f"192.168.1.{random.randint(1,254)}"
        event = random.choice(events)
        add_ids_event(ip,event[0],event[1])

# =======================
# Routes
# =======================
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    logs = Log.query.order_by(Log.timestamp.desc()).all()
    decrypted_logs = []

    port_scan = 0
    brute_force = 0
    malware = 0

    for log in logs:
        desc = decrypt_text(log.description)
        decrypted_logs.append({
            "id": log.id,
            "ip": log.ip_address,
            "event": log.event_type,
            "description": desc,
            "time": log.timestamp
        })

        if log.event_type == "Port Scan":
            port_scan += 1
        elif log.event_type == "Brute Force":
            brute_force += 1
        elif log.event_type == "Malware Activity":
            malware += 1

    return render_template(
        "dashboard.html",
        logs=decrypted_logs,
        port_scan=port_scan,
        brute_force=brute_force,
        malware=malware
    )

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/simulate")
def simulate():
    simulate_attack()
    return "Attack simulated"

@app.route("/generate")
def generate():
    generate_fake_logs(200)
    return "200 logs generated"

# =======================
# Initialize Database
# =======================
with app.app_context():
    db.create_all()

# =======================
# Run App (Railway Compatible)
# =======================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 🔹 البورت الديناميكي
    app.run(host="0.0.0.0", port=port, debug=True)  # 🔹 host 0.0.0.0 ليشتغل من الخارج