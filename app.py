from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def home():
    return jsonify({"service": "devops-ci-cd-demo", "status": "healthy"})


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
