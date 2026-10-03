import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Список популярных платформ для быстрой и надежной проверки
PLATFORMS = [
    {"name": "GitHub", "url": "https://github.com/{}", "error_code": 404},
    {"name": "Instagram", "url": "https://www.instagram.com/{}/", "error_code": 404},
    {"name": "Twitter / X", "url": "https://twitter.com/{}", "error_code": 404},
    {"name": "Telegram", "url": "https://t.me/{}", "error_code": 404},
    {"name": "TikTok", "url": "https://www.tiktok.com/@{}", "error_code": 404},
    {"name": "VK", "url": "https://vk.com/{}", "error_code": 404},
    {"name": "Reddit", "url": "https://www.reddit.com/user/{}", "error_code": 404},
    {"name": "Pinterest", "url": "https://www.pinterest.com/{}/", "error_code": 404},
    {"name": "Steam", "url": "https://steamcommunity.com/id/{}", "error_code": 404},
    {"name": "SoundCloud", "url": "https://soundcloud.com/{}", "error_code": 404}
]

@app.route('/')
def home():
    return "OSINT Backend is running!"

@app.route('/check', methods=['GET'])
def check_username():
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Username is required"}), 400

    results = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    for platform in PLATFORMS:
        target_url = platform["url"].format(username)
        try:
            response = requests.get(target_url, headers=headers, timeout=5)
            # Если страница существует (статус 200), значит аккаунт найден
            if response.status_code == 200:
                results.append({
                    "name": platform["name"],
                    "url": target_url
                })
        except Exception:
            continue

    return jsonify({"found": results})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    