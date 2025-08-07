from flask import Flask, request, jsonify
from flask_cors import CORS
import http.client
import json
import os
import gunicorn # Walaupun tidak dipanggil langsung, ini penting untuk Render

app = Flask(__name__)
CORS(app)

@app.route('/search', methods=['POST'])
def search_number():
    req_data = request.get_json()

    if not req_data or 'number' not in req_data:
        return jsonify({"error": "Nomor telepon tidak ditemukan"}), 400

    phone_number = req_data['number']
    
    conn = http.client.HTTPSConnection("truecaller16.p.rapidapi.com")

    # Ambil kunci API dari Environment Variable di Render
    api_key = os.environ.get('RAPIDAPI_KEY')
    if not api_key:
        return jsonify({"error": "Kunci API tidak diatur di server"}), 500

    headers = {
        'x-rapidapi-key': api_key,
        'x-rapidapi-host': "truecaller16.p.rapidapi.com"
    }

    conn.request("GET", f"/api/v1/search?number={phone_number}&code=62", headers=headers)

    res = conn.getresponse()
    data = res.read()
    
    try:
        response_data = json.loads(data.decode("utf-8"))
        return jsonify(response_data)
    except json.JSONDecodeError:
        return data.decode("utf-8")

# Bagian ini tidak diperlukan oleh Render karena Render akan menggunakan Gunicorn
# if __name__ == '__main__':

#     app.run(host='0.0.0.0', port=81)
