from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd
from pymongo import MongoClient
import pickle
from dotenv import load_dotenv
import os
load_dotenv()

conn_string = os.getenv('MONGODB_CONN_STR')
client = MongoClient(conn_string)

db = client['mdmmongodb-ale'] 
collection = db['FootballPredictor'] 

data_from_mongo = list(collection.find())

combined_df = pd.DataFrame(data_from_mongo)

features = ['Total_GF', 'Total_GA', 'PpG', 'Venue', 'cum_points', 'League Position', 'pointsLast3', 'avgGF', 'avgGA', 'pointsLastGame', 'GDlastGame', 'Market Value', 
            'Opponent_TotalGF', 'Opponent_TotalGA', 'OpponentPpG', 'Opponent_cum_points', 'Opponent_League Position', 'Opponent_pointsLast3', 'Opponent_avgGF', 'Opponent_avgGA', 
            'Opponent_pointsLastGame', 'Opponent_GDlastGame', 'Opponent_Market value']

target = 'points'  

X = combined_df[features]
y = combined_df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.4f}')
print(classification_report(y_test, y_pred))

with open('model.pkl', 'wb') as file:
    pickle.dump(clf, file)
