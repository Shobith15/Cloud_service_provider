import os
import time
import socket
import subprocess
from datetime import datetime

import psutil
from flask import Flask, jsonify, render_template, request, Response
from werkzeug.security import check_password_hash
import hmac

app = Flask(__name__)

START_TIME = time.time()

CUSTOMERS = {
    "client1": "/srv/client1",
    "client2": "/srv/client2",
}

MOUNTS = [
    "/", "/srv/client1", "/srv/client2", "/srv/backups"
]


def run_readonly(command):
    """Run a fixed, read-only system command without a shell."""
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=4,
            check=False
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return "Unavailable"
    except (OSError, subprocess.TimeoutExpired):
        return "Unavailable"


def service_status(name):
    result = run_readonly(["systemctl", "is-active", name])
    return "Running" if result == "active" else "Not running"


def get_system_info():
    memory = psutil.virtual_memory()
    boot_time = psutil.boot_time()
    uptime_seconds = int(time.time() - boot_time)

    return {
        "hostname": socket.gethostname(),
        "timestamp": datetime.now().astimezone().isoformat(),
        "cpu_percent": psutil.cpu_percent(interval=0.5),
        "memory": {
            "total_gb": round(memory.total / (1024 ** 3), 2),
            "used_gb": round(memory.used / (1024 ** 3), 2),
            "percent": memory.percent,
        },
        "uptime_seconds": uptime_seconds,
        "uptime_hours": round(uptime_seconds / 3600, 1),
    }


def get_disk_info():
    disks = []

    for mount in MOUNTS:
        try:
            usage = psutil.disk_usage(mount)
            disks.append({
                "mount": mount,
                "total_gb": round(usage.total / (1024 ** 3), 2),
                "used_gb": round(usage.used / (1024 ** 3), 2),
                "free_gb": round(usage.free / (1024 ** 3), 2),
                "percent": usage.percent,
            })
        except (OSError, PermissionError):
            disks.append({
                "mount": mount,
                "error": "Mount unavailable",
            })

    return disks


def get_customer_info():
    customers = []

    for customer, path in CUSTOMERS.items():
        public_path = os.path.join(path, "public")
        customers.append({
            "name": customer,
            "directory": path,
            "website_directory": public_path,
            "website_present": os.path.isfile(
                os.path.join(public_path, "index.html")
            ),
        })

    return customers


def get_storage_info():
    data_disk = run_readonly([
        "lsblk", "-dn", "-o", "NAME,SIZE", "/dev/sdb"
    ])

    logical_volumes = run_readonly([
        "lsblk", "-o", "NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS", "/dev/sdb"
    ])

    return {
        "data_disk": data_disk,
        "logical_volumes": logical_volumes,
    }


def get_backup_info():
    root = "/srv/backups/cloudguard"
    backups = []

    try:
        for name in sorted(os.listdir(root), reverse=True):
            path = os.path.join(root, name)

            if os.path.isdir(path):
                backups.append({
                    "name": name,
                    "created": datetime.fromtimestamp(
                        os.path.getmtime(path)
                    ).astimezone().isoformat(),
                })
    except (OSError, PermissionError):
        return {"available": False, "backups": []}

    return {
        "available": True,
        "count": len(backups),
        "backups": backups[:10],
    }


def get_service_info():
    return {
        service: service_status(service)
        for service in ("nginx", "ssh", "cron")
    }



@app.before_request
def require_dashboard_auth():
    username = os.environ.get("DASHBOARD_USERNAME")
    password_hash = os.environ.get("DASHBOARD_PASSWORD_HASH")

    if not username or not password_hash:
        return Response("Dashboard authentication is not configured.", 503)

    credentials = request.authorization

    if (
        credentials is None
        or not hmac.compare_digest(credentials.username, username)
        or not check_password_hash(password_hash, credentials.password)
    ):
        return Response(
            "Authentication required.",
            401,
            {"WWW-Authenticate": 'Basic realm="CloudGuard Admin"'}
        )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/overview")
def overview():
    return jsonify({
        "system": get_system_info(),
        "disks": get_disk_info(),
        "customers": get_customer_info(),
        "storage": get_storage_info(),
        "backups": get_backup_info(),
        "services": get_service_info(),
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "application": "CloudGuard Dashboard"})


if __name__ == "__main__":
    app.run()
