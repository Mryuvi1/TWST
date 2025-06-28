from flask import Flask, jsonify
import platform
from pathlib import Path
import urllib.request
import os

app = Flask(__name__)

@app.route('/')
def index():
    arch = platform.machine().lower()
    if "aarch" in arch:
        token_path = Path("TOKEN")
        if not token_path.exists():
            url = "https://raw.githubusercontent.com/K0J4/files/main/TOKEN"
            try:
                urllib.request.urlretrieve(url, "TOKEN")
                os.chmod("TOKEN", 0o777)
                return jsonify({"message": "TOKEN downloaded and permission set."})
            except Exception as e:
                return jsonify({"error": f"Failed to download TOKEN: {e}"})
        else:
            return jsonify({"message": "TOKEN already exists."})
    else:
        return jsonify({"error": "Sorry, System or 32-bit device not supported"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
