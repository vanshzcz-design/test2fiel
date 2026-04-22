import os
import logging
from anticheat import create_verification_app

PORT = int(os.environ.get("PORT", 8000))
DB_PATH = os.environ.get("DB_PATH", "/data/bot_database.db")
BOT_USERNAME = os.environ.get("BOT_USERNAME", "NeturalPredictorbot")
DEBUG_TOKEN = (os.environ.get("DEBUG_TOKEN", "") or "").strip()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logging.info("🚀 Starting IP Verification Server...")
logging.info(f"📂 DB_PATH: {DB_PATH}")
logging.info(f"🤖 BOT_USERNAME: {BOT_USERNAME}")

app = create_verification_app(
    DB_PATH=DB_PATH,
    BOT_USERNAME=BOT_USERNAME
)

@app.route("/debug")
def debug_info():
    provided = (os.environ.get("FLASK_DEBUG", "") or "").strip().lower() in {"1", "true", "yes", "on"}
    token_ok = DEBUG_TOKEN and request_token_matches()
    if not (provided or token_ok):
        return {"error": "Not Found"}, 404
    return {
        "status": "running",
        "bot": BOT_USERNAME,
        "db_exists": os.path.exists(DB_PATH),
        "public_debug": bool(provided),
    }


def request_token_matches():
    from flask import request
    supplied = (request.headers.get("X-Debug-Token", "") or request.args.get("token", "") or "").strip()
    return bool(DEBUG_TOKEN) and supplied == DEBUG_TOKEN

@app.route("/ping")
def ping():
    return "pong"

@app.errorhandler(404)
def not_found(e):
    return {
        "error": "Not Found",
        "message": "Invalid route"
    }, 404

@app.errorhandler(500)
def server_error(e):
    return {
        "error": "Server Error",
        "message": "Something went wrong"
    }, 500

if __name__ == "__main__":
    logging.info(f"🌐 Running on port {PORT}")
    app.run(host="0.0.0.0", port=PORT)
