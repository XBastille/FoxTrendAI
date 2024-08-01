import pandas as pd
import numpy as np
import optuna
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from sklearn.model_selection import train_test_split

class HousingPricePredictor:
    def __init__(self):
        self.optional_features=[
            "Resale", "MaintenanceStaff", "Gymnasium", "SwimmingPool", "LandscapedGardens",
            "JoggingTrack", "RainWaterHarvesting", "IndoorGames", "ShoppingMall",
            "Intercom", "SportsFacility", "ATM", "ClubHouse", "School",
            "24X7Security", "PowerBackup", "CarParking", "StaffQuarter",
            "Cafeteria", "MultipurposeRoom", "Hospital", "WashingMachine",
            "Gasconnection", "AC", "Wifi", "ChildrenPlayArea", "LiftAvailable",
            "BED", "VaastuCompliant", "Microwave", "GolfCourse", "TV",
            "DiningTable", "Sofa", "Wardrobe", "Refrigerator"
        ]
        self.mandatory_features=["Area", "No. of Bedrooms", "Latitude", "Longitude"]
        #self.mandatory_features=["Area", "No. of Bedrooms", "Resale", "Intercom", "Latitude", "Longitude"]
        self.dfs=self.load_data()
        self.merged_df=self.preprocess_data()
        self.feature_names=self.mandatory_features.copy()
        self.select_optional_features()
        self.X=self.merged_df[self.feature_names]
        self.y=self.merged_df["Price"]
        print(self.X.head())
        self.train_X, self.val_X, self.train_y, self.val_y=train_test_split(self.X, self.y, random_state=1)
        self.model=None

    def load_data(self):
        file_paths=[
            "intermediate-data/Mumbai_updated.csv",
            "intermediate-data/Delhi_updated.csv",
            "intermediate-data/Chennai_updated.csv",
            "intermediate-data/Hyderabad_updated.csv",
            "intermediate-data/Kolkata_updated.csv",
            "intermediate-data/Bangalore_updated.csv"
        ]
        dfs=[pd.read_csv(path) for path in file_paths]
        for df in dfs:
            df.drop(["Unnamed: 0"], axis=1, inplace=True)
        return dfs

    def preprocess_data(self):
        def preprocess(df):
            df=df.replace("NA", np.nan)
            df.dropna(subset=["Latitude"], inplace=True)
            df.dropna(subset=["Price"], inplace=True)
            df["Latitude"]=df["Latitude"].astype(float)
            df["Longitude"]=df["Longitude"].astype(float)
            return df
        map_dfs=[preprocess(df) for df in self.dfs]
        merged=pd.concat(map_dfs)
        merged=merged.rename(columns={"Children'splayarea": "ChildrenPlayArea"})
        merged=merged.dropna()
        return merged

    def optimize_model(self, n_trials=25):
        def objective(trial):
            param={
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
            model.fit(self.train_X, self.train_y)
            preds=model.predict(self.val_X)
            return np.sqrt(mean_squared_error(self.val_y, preds))

        study=optuna.create_study(direction="minimize")
        study.optimize(objective, n_trials=n_trials)
        best_params=study.best_trial.params
        self.model=XGBRegressor(**best_params)
        self.model.fit(self.train_X, self.train_y)
        print("Optimization complete. Best parameters:")
        for key, value in best_params.items():
            print(f"    {key}: {value}")

    def evaluate_model(self):
        preds=self.model.predict(self.val_X)
        mae=mean_absolute_error(self.val_y, preds)
        mse=mean_squared_error(self.val_y, preds)
        r2=r2_score(self.val_y, preds)
        print(f"MAE: {mae}")
        print(f"MSE: {mse}")
        print(f"R2: {r2}")

    def select_optional_features(self):
        print("Available optional features:")
        for i, feature in enumerate(self.optional_features, 1):
            print(f"{i}. {feature}")
        while True:
            try:
                choice=int(input("Select an optional feature to add (1-36), or 0 to finish: "))
                if choice==0:
                    break
                elif 1<=choice<=len(self.optional_features):
                    selected_feature=self.optional_features[choice-1]
                    if selected_feature not in self.feature_names:
                        self.feature_names.append(selected_feature)
                        print(f"Added feature: {selected_feature}")
                    else:
                        print(f"Feature {selected_feature} already selected.")
                else:
                    print("Invalid choice. Please select a number between 1 and 36.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def predict(self, input_features):
        input_df=pd.DataFrame([input_features], columns=self.feature_names)
        prediction=self.model.predict(input_df)
        return prediction[0]

if __name__=="__main__":
    predictor=HousingPricePredictor()
    predictor.optimize_model(n_trials=50)
    predictor.evaluate_model()
    while True:
        input_features={
            "Area": float(input("Enter the Area (in sq ft): ")),
            "No. of Bedrooms": int(input("Enter the number of bedrooms: ")),
            "Latitude": float(input("Enter the Latitude: ")),
            "Longitude": float(input("Enter the Longitude: "))
        }
        for feature in predictor.feature_names:
            if feature not in predictor.mandatory_features:
                input_features[feature]=int(input(f"Enter value for {feature} (1 for Yes, 0 for No): "))
        predicted_price=predictor.predict(input_features)
        print(f"The predicted housing price is: {predicted_price} lakhs")