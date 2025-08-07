from flask import Flask, request, jsonify
from flask_cors import CORS
import http.client
import json
import os # Kita bisa pakai os.environ lagi!

# Ganti nama 'app' menjadi 'api' agar dikenali Vercel
app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])
def search_number():
    # ... (kode di dalam fungsi ini sama persis seperti kode asli Anda)
    req_data = request.get_json()
    if not req_data or 'number' not in req_data:
        return jsonify({"error": "Nomor telepon tidak ditemukan"}), 400
    phone_number = req_data['number']

    conn = http.client.HTTPSConnection("truecaller16.p.rapidapi.com")
    api_key = os.environ.get('RAPIDAPI_KEY') # Ambil dari Vercel Env Vars
    if not api_key:
        return jsonify({"error": "Kunci API tidak diatur di server"}), 500

    headers = { 'x-rapidapi-key': api_key, 'x-rapidapi-host': "truecaller16.p.rapidapi.com" }
    conn.request("GET", f"/api/v1/search?number={phone_number}&code=62", headers=headers)
    res = conn.getresponse()
    data = res.read()

    try:
        return jsonify(json.loads(data.decode("utf-8")))
    except json.JSONDecodeError:
        return data.decode("utf-8")
