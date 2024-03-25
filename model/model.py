from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
from pymongo import MongoClient
import pickle
from dotenv import load_dotenv
import os
load_dotenv()

# MongoDB connection string
conn_string = os.getenv('MONGODB_CONN_STR')
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

# Assuming clf is your trained model
with open('model.pkl', 'wb') as file:
    pickle.dump(clf, file)
