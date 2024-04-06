import os
import pandas as pd
from pymongo import MongoClient
from azure.storage.blob import BlobServiceClient, BlobClient
import pickle
from flask import Flask, jsonify, request
from flask_cors import CORS
from pathlib import Path
from flask.helpers import send_file
import re 
from flask import send_from_directory

def load_model_from_blob():
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    if connection_string is None:
        raise Exception("Azure Storage Connection String is not set in environment variables.")
    
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    
    container_prefix = "footballpredictormodel"
    latest_suffix = -1
    latest_container = None

    containers = blob_service_client.list_containers(name_starts_with=container_prefix)
    for container in containers:
        match = re.search(f"{container_prefix}(\d+)", container['name'])
        if match:
            suffix = int(match.group(1))
            if suffix > latest_suffix:
                latest_suffix = suffix
                latest_container = container['name']

    if latest_container is None:
        raise Exception("No model container found.")

    print(f"Latest model container: {latest_container}")

    blob_name = "model.pkl"
    blob_client = blob_service_client.get_blob_client(container=latest_container, blob=blob_name)

    download_file_path = "model/model.pkl"
    print(f"Downloading model from Blob Storage: {latest_container}/{blob_name} to {download_file_path}")

    with open(download_file_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())

    with open(download_file_path, 'rb') as model_file:
        model = pickle.load(model_file)
    
    return model


app = Flask(__name__)
CORS(app)
app = Flask(__name__, static_url_path='/', static_folder='../frontend')

conn_string = os.getenv('MONGODB_CONN_STR')

def fetch_team_data(team_name):
    client = MongoClient(conn_string)
    db = client['mdmmongodb-ale']
    collection = db['FootballPredictor']
    team_data = list(collection.find({"Team": team_name}).sort([("Date", -1)]).limit(1))
    if team_data:
        return pd.DataFrame(team_data)
    else:
        return pd.DataFrame()

def predict_match_outcome(team_a_name, team_b_name, upcoming_match_venue):
    try:
        model = load_model_from_blob()
        print("*** Model loaded ***")
    except Exception as e:
        print(f"Failed to load model from Blob Storage: {e}")
    try:
        with open('model/model.pkl', 'rb') as file:
            model = pickle.load(file)
        print("*** Model loaded locally ***")
    except Exception as e:
        print(f"Failed to load model locally: {e}")
        raise
    model = load_model_from_blob()
    print("*** Model loaded ***")
    
    team_a_df = fetch_team_data(team_a_name)
    team_b_df = fetch_team_data(team_b_name)
    
    if team_a_df.empty or team_b_df.empty:
        return "Data for one or both teams not found."
    
    team_a_last_record = team_a_df.iloc[-1]
    team_b_last_record = team_b_df.iloc[-1]
    
    features_for_prediction = pd.DataFrame([{
        'Total_GF': team_a_last_record['Total_GF'],
        'Total_GA': team_a_last_record['Total_GA'],
        'PpG': team_a_last_record['PpG'],
        'Venue': upcoming_match_venue,
        'cum_points': team_a_last_record['cum_points'],
        'League Position': team_a_last_record['League Position'],
        'pointsLast3': team_a_last_record['pointsLast3'],
        'avgGF': team_a_last_record['avgGF'],
        'avgGA': team_a_last_record['avgGA'],
        'pointsLastGame': team_a_last_record['pointsLastGame'],
        'GDlastGame': team_a_last_record['GDlastGame'],
        'Market Value': team_a_last_record['Market Value'],
        'Opponent_TotalGF': team_b_last_record['Total_GF'],
        'Opponent_TotalGA': team_b_last_record['Total_GA'],
        'OpponentPpG': team_b_last_record['PpG'],
        'Opponent_cum_points': team_b_last_record['cum_points'],
        'Opponent_League Position': team_b_last_record['League Position'],
        'Opponent_pointsLast3': team_b_last_record['pointsLast3'],
        'Opponent_avgGF': team_b_last_record['avgGF'],
        'Opponent_avgGA': team_b_last_record['avgGA'],
        'Opponent_pointsLastGame': team_b_last_record['pointsLastGame'],
        'Opponent_GDlastGame': team_b_last_record['GDlastGame'],
        'Opponent_Market value': team_b_last_record['Market Value']  # Ensure this is 'Market Value' if using the same column name for both teams
}])
    
    predicted_points = model.predict(features_for_prediction)
    predicted_probabilities = model.predict_proba(features_for_prediction)
    
    confidence = max(predicted_probabilities[0])
    

    match_outcome = "draw" if predicted_points == 1 else "win" if predicted_points == 3 else "loss"
    confidence_percentage = f"{confidence * 100:.2f}%"
    return f"the model predicts a {match_outcome} for {team_a_name} against {team_b_name}.", f"With a confidence level of {confidence_percentage}"
    
@app.route("/")
def indexPage():
    frontend_dir = os.path.abspath("./frontend")
    return send_from_directory(frontend_dir, "index.html")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    team_a_name = data.get("team_a_name")
    team_b_name = data.get("team_b_name")
    venue = data.get("venue")


    outcome, confidence = predict_match_outcome(team_a_name, team_b_name, venue)
    
    return jsonify({"outcome": outcome, "confidence": confidence})

if __name__ == "__main__":
    app.run(debug=True)
