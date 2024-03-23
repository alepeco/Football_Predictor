from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
from pymongo import MongoClient

# MongoDB connection string
conn_string = "mongodb+srv://mongodb:<password>@mdmmongodb-ale.mongocluster.cosmos.azure.com/?tls=true&authMechanism=SCRAM-SHA-256&retrywrites=false&maxIdleTimeMS=120000"
client = MongoClient(conn_string)

# Specify the database and collection
db = client['mdmmongodb-ale']  # Replace with your actual database name
collection = db['FootballPredictor']  # Replace with your actual collection name

# Query the collection
data_from_mongo = list(collection.find())

# Convert to DataFrame
combined_df = pd.DataFrame(data_from_mongo)

# Note: You may need to clean or transform the data depending on its structure and your model's requirements

# Assuming 'combined_df' contains your complete dataset

# Feature selection: Specify the columns to be used as features
features = ['Total_GF', 'Total_GA', 'PpG', 'Venue', 'cum_points', 'League Position', 'pointsLast3', 'avgGF', 'avgGA', 'pointsLastGame', 'GDlastGame', 'Market Value', 
            'Opponent_TotalGF', 'Opponent_TotalGA', 'OpponentPpG', 'Opponent_cum_points', 'Opponent_League Position', 'Opponent_pointsLast3', 'Opponent_avgGF', 'Opponent_avgGA', 
            'Opponent_pointsLastGame', 'Opponent_GDlastGame', 'Opponent_Market value']  # Update this list based on your dataset

# Target variable
target = 'points'  # Ensure this column is in your DataFrame and properly coded as 0, 1, or 3

# Splitting the dataset into training and testing sets
X = combined_df[features]
y = combined_df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initializing and training the Random Forest classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Making predictions on the testing set
y_pred = clf.predict(X_test)

# Evaluating the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.4f}')
print(classification_report(y_test, y_pred))

import pandas as pd

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

