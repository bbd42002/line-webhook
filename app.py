from flask import Flask, request, jsonify
import json, os

app = Flask(__name__)
USER_IDS_FILE = "user_ids.json"

def load_ids():
    if os.path.exists(USER_IDS_FILE):
        with open(USER_IDS_FILE) as f:
            return json.load(f)
    return {}

def save_ids(data):
    with open(USER_IDS_FILE, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_json()
    for event in body.get("events", []):
        if event.get("source", {}).get("type") == "user":
            uid = event["source"]["userId"]
            ids = load_ids()
            ids[uid] = True
            save_ids(ids)
            print(f"已記錄 User ID：{uid}")
    return jsonify({"status": "ok"})

@app.route("/ids", methods=["GET"])
def get_ids():
    return jsonify(load_ids())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
