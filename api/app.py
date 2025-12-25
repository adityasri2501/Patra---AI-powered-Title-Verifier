from flask import Flask, request, jsonify
from flask_cors import CORS
from core.decision_engine import decide_title

app = Flask(__name__)
CORS(app)  # ✅ Frontend (5500) → Backend (5000) allow

@app.route("/verify", methods=["POST"])
def verify():
    data = request.get_json(force=True)
    title = data.get("title", "").strip()

    if not title:
        return jsonify({
            "status": "REJECTED",
            "reason": "Empty title not allowed"
        }), 400

    result = decide_title(title)
    return jsonify(result)

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "API running"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
