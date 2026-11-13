import os
import time
import hmac
import sqlite3
import urllib.request
import urllib.error

from datetime import datetime, timezone
from flask import Flask, jsonify, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

DATABASE = os.environ.get(
    "PORTAL_DATABASE",
    "/var/lib/cloudguard-portal/portal.db"
)

CUSTOMERS = {
    "client1": {
        "name": "Client One",
        "plan": "Business Starter",
        "price": 1499,
        "storage_gb": 8,
        "next_due": "2026-12-01",
        "domain": "client1.cloudguard.local",
        "website_path": "/srv/client1",
        "billing_status": "Paid",
        "invoices": [
            {"id": "INV-C1-003", "date": "2026-11-01", "amount": 1499, "status": "Paid"},
            {"id": "INV-C1-002", "date": "2026-10-01", "amount": 1499, "status": "Paid"},
            {"id": "INV-C1-001", "date": "2026-09-01", "amount": 1499, "status": "Paid"},
        ],
    },
    "client2": {
        "name": "Client Two",
        "plan": "Business Pro",
        "price": 2499,
        "storage_gb": 8,
        "next_due": "2026-12-01",
        "domain": "client2.cloudguard.local",
        "website_path": "/srv/client2",
        "billing_status": "Pending",
        "invoices": [
            {"id": "INV-C2-003", "date": "2026-11-01", "amount": 2499, "status": "Pending"},
            {"id": "INV-C2-002", "date": "2026-10-01", "amount": 2499, "status": "Paid"},
            {"id": "INV-C2-001", "date": "2026-09-01", "amount": 2499, "status": "Paid"},
        ],
    },
}

VALID_STATUSES = {"Open", "In Progress", "Resolved"}


def get_db():
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS support_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Open',
                admin_reply TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL
            )
        """)
        db.commit()


def current_customer():
    customer = request.headers.get("X-Portal-Customer", "")
    if customer not in CUSTOMERS:
        return None
    return customer


def website_health(customer):
    domain = CUSTOMERS[customer]["domain"]
    started = time.perf_counter()

    try:
        req = urllib.request.Request(
            "http://127.0.0.1/",
            headers={"Host": domain},
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=3) as response:
            elapsed = round((time.perf_counter() - started) * 1000)
            return {
                "status": "Online" if response.status < 500 else "Issue",
                "response_ms": elapsed,
            }
    except Exception:
        return {"status": "Offline", "response_ms": None}


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
        "application": "CloudGuard Customer Portal API"
    })


@app.get("/api/portal")
def portal_overview():
    customer = current_customer()
    if not customer:
        return jsonify({"error": "Customer context unavailable"}), 403

    details = CUSTOMERS[customer]
    health_info = website_health(customer)

    try:
        import shutil
        usage = shutil.disk_usage(details["website_path"])
        used_gb = round(usage.used / (1024 ** 3), 2)
    except OSError:
        used_gb = 0

    return jsonify({
        "customer": customer,
        "name": details["name"],
        "domain": details["domain"],
        "plan": details["plan"],
        "price": details["price"],
        "storage": {
            "limit_gb": details["storage_gb"],
            "used_gb": used_gb,
        },
        "website": health_info,
        "billing": {
            "status": details["billing_status"],
            "next_due": details["next_due"],
            "currency": "INR",
        },
        "invoices": details["invoices"],
        "demo_data": True,
    })


@app.post("/api/support")
def submit_support_request():
    customer = current_customer()
    if not customer:
        return jsonify({"error": "Customer context unavailable"}), 403

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise BadRequest("A JSON request body is required.")

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    subject = str(data.get("subject", "")).strip()
    message = str(data.get("message", "")).strip()

    if not all([name, email, subject, message]):
        return jsonify({"error": "Please complete all fields."}), 400

    if (
        len(name) > 80
        or len(email) > 120
        or len(subject) > 120
        or len(message) > 2000
        or "@" not in email
    ):
        return jsonify({"error": "Please check the field lengths and email address."}), 400

    created_at = datetime.now(timezone.utc).isoformat()

    with get_db() as db:
        cursor = db.execute("""
            INSERT INTO support_requests
            (customer, name, email, subject, message, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (customer, name, email, subject, message, created_at))
        request_id = cursor.lastrowid
        db.commit()

    return jsonify({
        "success": True,
        "message": "Your support request has been submitted.",
        "request_id": request_id,
    }), 201


def internal_authorized():
    if request.remote_addr not in ("127.0.0.1", "::1"):
        return False

    expected = os.environ.get("PORTAL_ADMIN_TOKEN", "")
    supplied = request.headers.get("Authorization", "")
    supplied = supplied.removeprefix("Bearer ")

    return bool(expected) and hmac.compare_digest(expected, supplied)


@app.get("/internal/support")
def admin_support_requests():
    if not internal_authorized():
        return jsonify({"error": "Unauthorized"}), 401

    with get_db() as db:
        rows = db.execute("""
            SELECT * FROM support_requests
            ORDER BY id DESC
        """).fetchall()

    return jsonify([dict(row) for row in rows])


@app.patch("/internal/support/<int:request_id>")
def update_support_request(request_id):
    if not internal_authorized():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "A JSON request body is required"}), 400

    status = str(data.get("status", "")).strip()
    reply = str(data.get("admin_reply", "")).strip()

    if status not in VALID_STATUSES or len(reply) > 2000:
        return jsonify({"error": "Invalid status or reply"}), 400

    with get_db() as db:
        cursor = db.execute("""
            UPDATE support_requests
            SET status = ?, admin_reply = ?
            WHERE id = ?
        """, (status, reply, request_id))
        db.commit()

    if cursor.rowcount == 0:
        return jsonify({"error": "Request not found"}), 404

    return jsonify({"success": True, "id": request_id, "status": status})


initialize_database()


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)
