from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
from pymongo import MongoClient
import pickle

"""
def load_model():
    with open('model.pkl', 'rb') as file:
        clf = pickle.load(file)
    return clf

clf = load_model()

# MongoDB connection string
conn_string = "mongodb+srv://mongodb:Larva72992!$!@mdmmongodb-ale.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
client = MongoClient(conn_string)

# Specify the database and collection
db = client['mdmmongodb-ale']  # Replace with your actual database name
collection = db['FootballPredictor']  # Replace with your actual collection name

# Query the collection
data_from_mongo = list(collection.find())

# Convert to DataFrame
combined_df = pd.DataFrame(data_from_mongo)

# Example: Let's say you want to predict the outcome of a match between "Team A" and "Team B"
team_a_name = "Barcelona"
team_b_name = "Celta Vigo"

# Step 1: Identify the last records for both teams
team_a_last_record = combined_df[combined_df['Team'] == team_a_name].iloc[-1]
team_b_last_record = combined_df[combined_df['Team'] == team_b_name].iloc[-1]
upcoming_match_venue = 1
# Step 2: Prepare the feature vector for prediction
# This should include features from both teams' last records.
# For simplicity, let's assume your model uses 'Last_GF', 'Last_GA', 'avgGF', 'avgGA' for both home and away teams
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

# Making a prediction with probabilities
predicted_probabilities = clf.predict_proba(features_for_prediction)

# Assuming the classes are ordered as [0, 1, 3] for [loss, draw, win]
print(f"Model's confidence in prediction (Loss, Draw, Win): {predicted_probabilities}")

# Continuing with the previous example
predicted_points = clf.predict(features_for_prediction)
match_outcome = "draw" if predicted_points == 1 else "win" if predicted_points == 3 else "loss"
print(f"The model predicts a {match_outcome} for {team_a_name} against {team_b_name}.")

"""
# model.py
import pandas as pd
from pymongo import MongoClient
import pickle
import os
from dotenv import load_dotenv
load_dotenv()

# Load model function
def load_model():
    with open('model.pkl', 'rb') as file:
        clf = pickle.load(file)
    return clf

# MongoDB connection string
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
    clf = load_model()
    
    # Fetch the last record for both teams
    team_a_df = fetch_team_data(team_a_name)
    team_b_df = fetch_team_data(team_b_name)
    
    if team_a_df.empty or team_b_df.empty:
        return "Data for one or both teams not found."
    
    team_a_last_record = team_a_df.iloc[-1]
    team_b_last_record = team_b_df.iloc[-1]
    
    # Prepare the feature vector for prediction
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
    
    predicted_points = clf.predict(features_for_prediction)
    predicted_probabilities = clf.predict_proba(features_for_prediction)
    
    # Assuming the classes are ordered as [0, 1, 3] for [loss, draw, win]
    # Extracting the highest probability as confidence
    confidence = max(predicted_probabilities[0])
    

    # Translate predicted points to match outcome
    match_outcome = "draw" if predicted_points == 1 else "win" if predicted_points == 3 else "loss"
    # Convert confidence to a percentage string with 2 decimal places
    confidence_percentage = f"{confidence * 100:.2f}%"
    return f"The model predicts a {match_outcome} for {team_a_name} against {team_b_name}.", f"with a confidence level of {confidence_percentage}"
