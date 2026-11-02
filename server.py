import os
from datetime import datetime, timezone
from threading import Lock
from flask import Flask, jsonify, request

app = Flask(__name__)
API_KEY = os.environ.get("GSP_API_KEY", "")
latest = {}
lock = Lock()

@app.after_request
def add_cors(response):
    origin = request.headers.get("Origin", "")
    # Public dashboard reads only market data. Restrict this to your deployed site in production.
    allowed = os.environ.get("GSP_ALLOWED_ORIGIN", "*")
    response.headers["Access-Control-Allow-Origin"] = allowed if allowed != "*" else "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-API-Key"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Cache-Control"] = "no-store"
    return response

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "service": "GOLD SCALPING PRO bridge API"})

@app.route("/api/bridge/tick", methods=["POST", "OPTIONS"])
def ingest_tick():
    if request.method == "OPTIONS":
        return ("", 204)
    if not API_KEY:
        return jsonify({"ok": False, "error": "Server API key is not configured"}), 503
    if request.headers.get("X-API-Key", "") != API_KEY:
        return jsonify({"ok": False, "error": "Unauthorized"}), 401
    body = request.get_json(silent=True) or {}
    platform = str(body.get("platform", "")).lower()
    symbol = str(body.get("symbol", ""))
    try:
        bid, ask = float(body["bid"]), float(body["ask"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"ok": False, "error": "bid and ask must be numeric"}), 400
    if platform not in ("mt4", "mt5") or not symbol or bid <= 0 or ask <= 0 or ask < bid:
        return jsonify({"ok": False, "error": "Invalid platform, symbol, bid or ask"}), 400
    record = {
        "platform": platform, "symbol": symbol, "bid": bid, "ask": ask,
        "price": (bid + ask) / 2,
        "updated_at": datetime.now(timezone.utc).isoformat()
    }
    with lock:
        latest[platform] = record
    return jsonify({"ok": True, "received": record})

@app.route("/api/market", methods=["GET"])
def market():
    platform = request.args.get("platform", "mt5").lower()
    if platform not in ("mt4", "mt5"):
        return jsonify({"ok": False, "error": "platform must be mt4 or mt5"}), 400
    with lock:
        record = latest.get(platform)
    if not record:
        return jsonify({"ok": True, "connected": False, "platform": platform,
                        "message": "Belum ada tick diterima dari EA."})
    return jsonify({"ok": True, "connected": True, **record})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8080")))
