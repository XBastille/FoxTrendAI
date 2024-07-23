import numpy as np
import pandas as pd
import optuna
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

class UsedCarPricePredictor:
    def __init__(self, data_path):
        self.df=pd.read_csv(data_path)
        self.encoders={}
        self.preprocess_data()
        self.X_train, self.X_test, self.y_train, self.y_test=self.prepare_data()
        self.scaler=StandardScaler()
        self.X_train_scaled=self.scaler.fit_transform(self.X_train)
        self.X_test_scaled=self.scaler.transform(self.X_test)
        self.model=None

    def preprocess_data(self):
        drop_columns=["id", "region", "region_url", "model", "description", "state", "county",
        "posting_date", "url", "title_status", "VIN", "size", "image_url", "lat", "long"]
        self.df.drop(columns=drop_columns, inplace=True)
        self.df.dropna(inplace=True)
        numerics=["int8", "int16", "int32", "int64", "float16", "float32", "float64"]
        categorical_columns=[]
        features=self.df.columns.values.tolist()
        categorical_columns.extend(col for col in features if self.df[col].dtype not in numerics)
        for col in categorical_columns:
            if col in self.df.columns:
                le=LabelEncoder()
                le.fit(list(self.df[col].astype(str).values))
                self.df[col]=le.transform(list(self.df[col].astype(str).values))
                self.encoders[col]=le
        self.df["year"]=(self.df["year"]-1900).astype(int)
        self.df["odometer"]=self.df["odometer"].astype(int)
        self.df=self.df[self.df["price"]>1000]
        self.df=self.df[self.df["price"]<40000]
        self.df["odometer"]=self.df["odometer"]//5000
        self.df=self.df[self.df["year"]>110]

    def prepare_data(self):
        X=self.df.drop(columns=["price"])
        y=self.df["price"]
        X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.2, random_state=0)
        return X_train, X_test, y_train, y_test

    def objective(self, trial):
        param={
            "objective":"reg:squarederror",
            "eval_metric":"rmse",
            "n_estimators":trial.suggest_int("n_estimators", 100, 1000),
            "max_depth":trial.suggest_int("max_depth", 3, 10),
            "learning_rate":trial.suggest_float("learning_rate", 0.01, 0.1),
            "subsample":trial.suggest_float("subsample", 0.6, 1.0),
            "colsample_bytree":trial.suggest_float("colsample_bytree", 0.6, 1.0),
            "reg_alpha":trial.suggest_float("reg_alpha", 0, 10),
            "reg_lambda":trial.suggest_float("reg_lambda", 0, 10),
            "verbosity":0,
        }
        model=XGBRegressor(**param)
        model.fit(self.X_train_scaled, self.y_train)
        preds=model.predict(self.X_test_scaled)
        return np.sqrt(mean_squared_error(self.y_test, preds))

    def optimize_model(self, n_trials=25):
        study=optuna.create_study(direction="minimize")
        study.optimize(self.objective, n_trials=n_trials)
        best_params=study.best_trial.params
        self.model=XGBRegressor(**best_params)
        self.model.fit(self.X_train_scaled, self.y_train)
        print("Optimization complete. Best parameters:")
        for key, value in best_params.items():
            print(f" {key}: {value}")

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
        numerics=["int8", "int16", "int32", "int64", "float16", "float32", "float64"]
        categorical_columns=[]
        features=input_df.columns.values.tolist()
        categorical_columns.extend(col for col in features if input_df[col].dtype not in numerics)
        for col in categorical_columns:
            if col in input_df.columns and col in self.encoders:
                le=self.encoders[col]
                input_df[col]=le.transform(list(input_df[col].astype(str).values))
        input_df["year"]=(input_df["year"]-1900).astype(int)
        input_df["odometer"]=input_df["odometer"].astype(int)//5000
        input_scaled=self.scaler.transform(input_df)
        prediction=self.model.predict(input_scaled)
        return prediction[0]

if __name__=="__main__":
    predictor=UsedCarPricePredictor("Vehicles_US.csv")
    predictor.optimize_model(n_trials=25)
    predictor.evaluate_model()
    while True:
        input_features={
            "year":int(input("Enter the Year: ")),
            "manufacturer":input("Enter the Manufacturer: "),
            "condition":input("Enter the Condition: "),
            "cylinders":input("Enter the Number of Cylinders (formant: 'n cylinders'): "),
            "fuel":input("Enter the Fuel Type: "),
            "odometer":float(input("Enter the Odometer Reading: ")),
            "transmission":input("Enter the Transmission Type: "),
            "drive":input("Enter the Drive Type: "),
            "type":input("Enter the Type: "),
            "paint_color":input("Enter the Paint Color: "),
        }
        predicted_price=predictor.predict(input_features)
        print(f"The predicted used car price is: ${predicted_price:.2f}")
