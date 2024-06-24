import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, make_scorer
from sklearn.model_selection import GridSearchCV

# Load and prepare the data
data = pd.read_csv("final.csv")
df = pd.DataFrame(data)

# Fill missing values with 0
df = df.fillna(0)

# Feature columns to determine
features = ["Age", "G", "GS", "MP", "FG", "FGA", 'FG%', '3P', '3PA', '3P%', '2P', '2PA', '2P%', 'eFG%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'W', 'L', 'W/L%', 'GB', 'PS/G', 'PA/G', 'SRS']

# Split the data into training and test sets
train = df[~(df["Year"] == 2021)]
test = df[df["Year"] == 2021]

# Define Linear Regression model
linear_model = LinearRegression()

# Scoring algorithm to find average precision score
def find_ap(combination):
    """
    Calculate the average precision score of the top 5 predicted players.
    
    Parameters:
    - combination: DataFrame containing actual and predicted MVP shares.
    
    Returns:
    - Average precision score.
    """
    actual = combination.sort_values("Share", ascending=False).head(5)
    predicted = combination.sort_values("pred", ascending=False)
    ps = []
    found = 0
    seen = 1
    for index, row in predicted.iterrows():
        if row["Player"] in actual["Player"].values:
            found += 1
            ps.append(found / seen)
        seen += 1
    return sum(ps) / len(ps) if ps else 0

def train_and_evaluate(model, train, test, features):
    """
    Train the model and evaluate its performance on the test set.
    
    Parameters:
    - model: The regression model to train.
    - train: The training dataset.
    - test: The test dataset.
    - features: The list of feature columns.
    
    Returns:
    - mse: The mean squared error of the model on the test set.
    - ap: The average precision score of the model.
    - combination: DataFrame combining the test set with predictions.
    """
    model.fit(train[features], train["Share"])
    pred = model.predict(test[features])
    pred_df = pd.DataFrame(pred, columns=["pred"], index=test.index)
    combination = pd.concat([test[["Player", "Share"]], pred_df], axis=1)
    mse = mean_squared_error(combination["Share"], combination["pred"])
    ap = find_ap(combination)
    return mse, ap, combination

# Function to perform hyperparameter tuning using GridSearchCV
def tune_model(model, params, train, features):
    """
    Tune the hyperparameters of a model using GridSearchCV.
    
    Parameters:
    - model: The regression model to tune.
    - params: The parameter grid for the model.
    - train: The training dataset.
    - features: The list of feature columns.
    
    Returns:
    - The best model after tuning.
    """
    grid_search = GridSearchCV(model, params, scoring=make_scorer(mean_squared_error, greater_is_better=False), cv=5)
    grid_search.fit(train[features], train["Share"])
    return grid_search.best_estimator_

# Define parameter grid for Linear Regression (here, no hyperparameters to tune explicitly)
linear_params = {}

# Tune the Linear Regression model and evaluate
best_linear_model = tune_model(linear_model, linear_params, train, features)
mse, ap, combination = train_and_evaluate(best_linear_model, train, test, features)
print(f"Best Linear Regression Model")
print(combination.sort_values("pred", ascending=False).head(20))
print(f"MSE: {mse}")
print(f"AP: {ap}")
print("---------------------------")

# Calculate average AP across multiple years for the Linear Regression model
def evaluate_model_over_years(model, df, features):
    """
    Evaluate the model over multiple years and calculate average AP scores.
    
    Parameters:
    - model: The tuned model.
    - df: The entire dataset.
    - features: The list of feature columns.
    
    Returns:
    - Average AP score for the model.
    """
    results = []
    years = list(range(1991, 2022))
    for year in years[5:]:
        train = df[df["Year"] < year]
        test = df[df["Year"] == year]
        _, ap, _ = train_and_evaluate(model, train, test, features)
        results.append(ap)
    avg_result = sum(results) / len(results)
    return avg_result

avg_ap = evaluate_model_over_years(best_linear_model, df, features)
print("Average AP over multiple years for the best Linear Regression model:")
print(avg_ap)

# Add feature importance analysis
def analyze_feature_importance(model, features):
    """
    Analyze feature importance based on model coefficients.
    
    Parameters:
    - model: The trained regression model.
    - features: The list of feature columns.
    
    Returns:
    - DataFrame with feature names and their corresponding coefficients.
    """
    feature_importance = pd.DataFrame({
        'Feature': features,
        'Coefficient': model.coef_
    })
    feature_importance = feature_importance.sort_values(by='Coefficient', ascending=False)
    return feature_importance

# Display feature importance for the best Linear Regression model
feature_importance = analyze_feature_importance(best_linear_model, features)
print("Feature Importance:")
print(feature_importance)

# Apply add_ranks function to the first prediction
def add_ranks(predictions):
    """
    Add ranking differences between actual and predicted MVP shares.
    
    Parameters:
    - predictions: DataFrame containing actual and predicted MVP shares.
    
    Returns:
    - DataFrame with added ranking columns and differences.
    """
    predictions = predictions.sort_values("pred", ascending=False)
    predictions["Predicted_Rk"] = list(range(1, predictions.shape[0] + 1))
    predictions = predictions.sort_values("Share", ascending=False)
    predictions["Rk"] = list(range(1, predictions.shape[0] + 1))
    predictions["Diff"] = predictions["Rk"] - predictions["Predicted_Rk"]
    return predictions

# Display the rankings with differences for the best Linear Regression model
print(add_ranks(combination))
