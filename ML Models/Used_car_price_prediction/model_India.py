import numpy as np
import pandas as pd
import optuna
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

class UsedCarPricePredictor:
    def __init__(self, data_path):
        self.df=pd.read_csv(data_path)
        self.preprocess_data()
        self.X_train, self.X_test, self.y_train, self.y_test=self.prepare_data()
        self.scaler=StandardScaler()
        self.X_train_scaled=self.scaler.fit_transform(self.X_train)
        self.X_test_scaled=self.scaler.transform(self.X_test)
        self.model=None

    def preprocess_data(self):
        self.df.drop(columns=["Unnamed: 0", "New_Price"], inplace=True)
        self.df["Mileage"]=self.df["Mileage"].str.split().str[0].astype(float)
        self.df["Engine"]=self.df["Engine"].str.split().str[0].astype(float)
        self.df["Power"]=self.df["Power"].str.replace("null bhp", "NaN").str.split().str[0].astype(float)
        self.df["Mileage"].fillna(self.df["Mileage"].median(), inplace=True)
        self.df["Engine"].fillna(self.df["Engine"].median(), inplace=True)
        self.df["Power"].fillna(self.df["Power"].median(), inplace=True)
        self.df["Seats"].fillna(self.df["Seats"].median(), inplace=True)
        self.df["Car_Age"]=2024-self.df["Year"]
        self.df["Mileage_to_Engine_Ratio"]=self.df["Mileage"]/self.df["Engine"]
        self.df["Power_to_Engine_Ratio"]=self.df["Power"]/self.df["Engine"]
        self.df["Brand"]=self.df["Name"].str.split().str[0]
        self.df["Is_Vintage"]=self.df["Car_Age"].apply(lambda x: 1 if x>25 else 0)
        self.df["Kms_per_Year"]=self.df["Kilometers_Driven"]/self.df["Car_Age"]
        self.df=pd.get_dummies(self.df, columns=["Location", "Fuel_Type", "Transmission", "Owner_Type", "Brand"], drop_first=True)

    def prepare_data(self):
        X=self.df.drop(columns=["Name", "Price", "Year"])
        y=self.df["Price"]
        X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.2, random_state=42)
        return X_train, X_test, y_train, y_test

    def objective(self, trial):
        param = {
            "objective": "reg:squarederror",
            "eval_metric": "rmse",
            "n_estimators": trial.suggest_int("n_estimators", 100, 1000),
            "max_depth": trial.suggest_int("max_depth", 3, 10),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.1),
            "subsample": trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "reg_alpha": trial.suggest_float("reg_alpha", 0, 10),
            "reg_lambda": trial.suggest_float("reg_lambda", 0, 10),
            "verbosity": 0,
        }
        model=XGBRegressor(**param)
        model.fit(self.X_train_scaled, self.y_train)
        preds=model.predict(self.X_test_scaled)
        return np.sqrt(mean_squared_error(self.y_test, preds))

    def optimize_model(self, n_trials=50):
        study=optuna.create_study(direction="minimize")
        study.optimize(self.objective, n_trials=n_trials)
        best_params=study.best_trial.params
        self.model=XGBRegressor(**best_params)
        self.model.fit(self.X_train_scaled, self.y_train)
        print("Optimization complete. Best parameters:")
        for key, value in best_params.items():
            print(f"    {key}: {value}")

    def evaluate_model(self):
        y_pred=self.model.predict(self.X_test_scaled)
        mae=mean_absolute_error(self.y_test, y_pred)
        mse=mean_squared_error(self.y_test, y_pred)
        rmse=np.sqrt(mse)
        r2=r2_score(self.y_test, y_pred)
        print(f"MAE: {mae}")
        print(f"MSE: {mse}")
        print(f"RMSE: {rmse}")
        print(f"R2: {r2}")

    def predict(self, input_features):
        input_df=pd.DataFrame([input_features])
        input_df["Car_Age"]=2024-input_df["Year"]
        input_df["Mileage_to_Engine_Ratio"]=input_df["Mileage"]/input_df["Engine"]
        input_df["Power_to_Engine_Ratio"]=input_df["Power"]/input_df["Engine"]
        input_df["Is_Vintage"]=input_df["Car_Age"].apply(lambda x: 1 if x>25 else 0)
        input_df["Kms_per_Year"]=input_df["Kilometers_Driven"]/input_df["Car_Age"]
        brand_col=f"Brand_{input_features['Brand']}"
        transmission_col=f"Transmission_{input_features['Transmission']}"
        Owner_Type_col=f"Owner_Type_{input_features['Owner_Type']}"
        Fuel_Type_col=f"Fuel_Type_{input_features['Fuel_Type']}"
        Location_col=f"Location_{input_features['Location']}"
        Seats_col=f"Seats_{input_features['Seats']}"
        for col in self.X_train.columns:
            if col not in input_df.columns:
                input_df[col]=1 if col in [brand_col, transmission_col, Owner_Type_col, Fuel_Type_col, Location_col, Seats_col] else 0
        input_df=input_df[self.X_train.columns]
        input_df.to_csv("input_example.csv")
        input_scaled=self.scaler.transform(input_df)
        prediction=self.model.predict(input_scaled)
        return prediction[0]

if __name__=="__main__":
    predictor=UsedCarPricePredictor("vehicle_US.csv")
    predictor.optimize_model(n_trials=50)
    predictor.evaluate_model()
    while True:
        input_features={
            "Brand": input("Enter the Brand: "),
            "Power": float(input("Enter the Power (in bhp): ")),
            "Year": int(input("Enter the Year: ")),
            "Seats": int(input("Enter the No. of seats: ")),
            "Engine": float(input("Enter the Engine (in CC): ")),
            "Transmission": input("Enter the Transmission (Manual/Automatic): "),
            "Kilometers_Driven": float(input("Enter the Kilometers Driven: ")),
            "Location": input("Enter the Location: "),
            "Fuel_Type": input("Enter the Fuel_type: "),
            "Owner_Type": input("Enter the Owner_Type: "),
            "Mileage": float(input("Enter the Mileage (in kmpl): "))
        }
        predicted_price=predictor.predict(input_features)
        print(f"The predicted used car price is: {predicted_price} lakhs")
