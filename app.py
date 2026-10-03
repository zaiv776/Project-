import subprocess
import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Sherlock Backend is running!"

@app.route('/check', methods=['GET'])
def check_username():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    try:
        # Запуск утилиты sherlock через командную строку с сохранением в json
        cmd = f"sherlock {username} --json --output result.json"
        subprocess.run(cmd, shell=True, capture_output=True, text=True)

        results = []
        json_file = f"{username}.json"
        
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for site, info in data.items():
                    if info.get("status") == "Found":
                        results.append({
                            "name": site,
                            "url": info.get("url_user")
                        })
            os.remove(json_file)
        
        if os.path.exists("result.json"):
            os.remove("result.json")

        return jsonify({"found": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    