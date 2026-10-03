from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)
# Простой список платформ для демонстрации бэкенда (можно расширить)
PLATFORMS = [
    {"name": "GitHub", "url": lambda u: f"https://github.com/{u}", "api": lambda u: f"https://api.github.com/users/{u}"},
    {"name": "Reddit", "url": lambda u: f"https://www.reddit.com/user/{u}", "api": lambda u: f"https://www.reddit.com/user/{u}/about.json"}
]

@app.route('/')
def home():
    return "Sherlock Backend is running!"

@app.route('/check', methods=['GET'])
def check_username():
    username = request.args.get('username', '').strip()
    if not username:
        return jsonify({"error": "No username provided"}), 400

    found_results = []
    
    # Проверяем сайты через сервер (сервер не имеет проблем с CORS)
    for p in PLATFORMS:
        try:
            res = requests.get(p["api"](username), timeout=5, headers={"User-Agent": "Mozilla/5.0"})
            if res.status_code == 200:
                data = res.json()
                # Простейшая валидация ответа API
                if data and data.get("message") != "Not Found":
                    found_results.append({
                        "name": p["name"],
                        "url": p["url"](username)
                    })
        except Exception as e:
            pass

    return jsonify({
        "username": username,
        "found": found_results
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
