import numpy as np
import pandas as pd
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import optuna

class HousingPriceModel:
    def __init__(self, data_path):
        self.data_path=data_path
        self.df=pd.read_csv(self.data_path, encoding="ISO-8859-1")
        self.le_city=LabelEncoder()
        self.le_province=LabelEncoder()
        self.scaler=StandardScaler()
        self.model=None
        self.best_params=None

    def preprocess_data(self):
        df=self.df.copy()
        df["City"]=self.le_city.fit_transform(df["City"])
        df["Province"]=self.le_province.fit_transform(df["Province"])
        df.drop(["Address", "Latitude", "Longitude"], axis=1, inplace=True)
        X, y=df.drop(["Price"], axis=1), df["Price"]
        print(X.head())
        X=self.scaler.fit_transform(X)
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def objective(self, trial):
        param={
            'objective': 'reg:squarederror',
            'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
            'max_depth': trial.suggest_int('max_depth', 3, 10),
            'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
            'subsample': trial.suggest_float('subsample', 0.5, 1.0),
            'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
            'reg_alpha': trial.suggest_float('reg_alpha', 0, 10),
            'reg_lambda': trial.suggest_float('reg_lambda', 0, 10),
        }
        model=XGBRegressor(**param)
        model.fit(self.X_train, self.y_train)
        preds=model.predict(self.X_test)
        return np.sqrt(mean_squared_error(self.y_test, preds))

    def optimize_hyperparameters(self, n_trials=25):
        self.X_train, self.X_test, self.y_train, self.y_test=self.preprocess_data()
        study=optuna.create_study(direction='minimize')
        study.optimize(self.objective, n_trials=n_trials)
        self.best_params=study.best_trial.params

    def train_final_model(self):
        self.model=XGBRegressor(**self.best_params)
        self.model.fit(self.X_train, self.y_train)

    def evaluate_model(self):
        y_pred=self.model.predict(self.X_test)
        mae=mean_absolute_error(self.y_test, y_pred)
        mse=mean_squared_error(self.y_test, y_pred)
        r2=r2_score(self.y_test, y_pred)
        print("Evaluation Metrics:")
        print(f"Mean Absolute Error (MAE): {mae}")
        print(f"Mean Squared Error (MSE): {mse}")
        print(f"R-squared (R2): {r2}")

    def preprocess_input(self, input_data):
        input_df=pd.DataFrame([input_data])
        input_df['City']=self.le_city.transform(input_df['City'])
        input_df['Province']=self.le_province.transform(input_df['Province'])
        print(input_df)
        input_data=self.scaler.transform(input_df)
        return input_data

    def predict(self, input_data):
        input_data=self.preprocess_input(input_data)
        return self.model.predict(input_data)

data_path="estate_CA.csv"
model=HousingPriceModel(data_path)
model.optimize_hyperparameters(n_trials=25)
model.train_final_model()
model.evaluate_model()
while True:
    user_input={
        "City": input("Enter the city: "),
        "Number_Beds": float(input("Enter the number of bedrooms: ")),
        "Number_Baths": float(input("Enter the number of bathrooms: ")),
        "Province": input("Enter the province: "),
        "Population": int(input("Enter the population: ")),
        "Median_Family_Income": float(input("Enter the median family income: "))
    }
    predicted_price=model.predict(user_input)
    print(f"Predicted Price: {predicted_price}")
