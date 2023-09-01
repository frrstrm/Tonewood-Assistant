# Author: Dakota Farrstrom
# Date: 08/19/2023

import pandas as pd
from IPython.core.display_functions import display
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Import Instrument Database file as Pandas DataFrame
df = pd.read_csv('static/TAdata.csv')

# Key Instrument Tonality Characteristics used for Customer Form
us = df[['RatingClass', 'BodyStyle', 'TopWood', 'BackSideWood', 'Cutaway', 'Finish']]

# Nominal version of Key Instrument Tonality Characteristics used for Customer Form
usn = df[['RatingClass', 'BodyStyle', 'TopWood', 'BackSideWood', 'Cutaway', 'Finish']]


# Main parameters for customer input and Random Forest reference
def main(bs, tw, bsw, ca, f):
    keys = us.loc[
        (us['BodyStyle'] == bs) &
        (us['TopWood'] == tw) &
        (us['BackSideWood'] == bsw) &
        (us['Cutaway'] == ca) &
        (us['Finish'] == f)
        ]
    print(keys)
    return keys


def createDF(BodyStyle, TopWood, BackSideWood, Cutaway, Finish):
    userSet = main(BodyStyle, TopWood, BackSideWood, Cutaway, Finish)
    return userSet


# Encode non-numeric data into ordinal encoding for algorithm processing
LE = preprocessing.LabelEncoder()
for column in us.columns:
    us[column] = LE.fit_transform(us[column])
display(us)


# Main code for Tonewood Assistant Identification/Classification application functionality
def identify(userSet):
    try:
        # Remove Rating Class from the User-Set dataframe
        X = userSet.drop(['RatingClass'], axis=1)  # Data to reference
        y = userSet["RatingClass"]  # Value to predict
        print(X)
        print(y)
        # Train-Test data setup
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42, test_size=.5, train_size=.5)
        rf = RandomForestClassifier(n_estimators=100, random_state=42)  # Random Forest ML Model
        rf.fit(X_train, y_train)  # Fitting training data to Random Forest model
        # Accuracy score
        accuracy = round(rf.score(X_test, y_test) * 100, 2)
        preds = list(rf.predict(X_test))
        print(preds)
        if preds[0] == 1:
            predictedRating = 'Selected Tonewoods will likely result in an optimal tonality! '
        else:
            predictedRating = ('Selected Tonewoods will likely result in an less optimal tonality. That said, we have seen unicorns!'
                               '\nPlease contact the Sales Team for further discussion!')
        predictions = int(len(preds))
        message = "Predicted Overall Guitar Rating: {}".format(
            predictedRating) + "<br>Prediction accuracy was {}%".format(
            accuracy) + " correct for {}".format(predictions) + " reference guitars."
        if predictions > 0:
            return message
        else:
            return 'Data Insufficiency'
    except ValueError:
        return 'No matching instruments with this option set. Please select an alternative Tonewood configuration.'
