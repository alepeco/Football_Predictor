# app.py
from flask import Flask, request, jsonify
from backend.model import predict_match_outcome
from flask.helpers import send_file

app = Flask(__name__, static_url_path='/', static_folder='frontend')

@app.route("/")
def indexPage():
     return send_file("frontend/index.html")  

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    team_a_name = data['team_a_name']
    team_b_name = data['team_b_name']
    venue = data['venue']
    
    confidence, outcome = predict_match_outcome(team_a_name, team_b_name, venue)

    # Include both outcome and confidence in the response
    return jsonify({
        'outcome': outcome,
        'confidence': confidence
    })

if __name__ == '__main__':
    app.run(debug=True)
