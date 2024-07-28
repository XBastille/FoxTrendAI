import numpy as np
import pandas as pd
import optuna
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor

class DataTransformation:
    def __init__(self, data_path):
        self.df=pd.read_csv(data_path)
        self.encoders={}
        self.preprocess_data()

    def preprocess_data(self):
        drop_columns=["id", "vin", "stock_no", "trim", "seller_name", "street", "city", "state", "zip", "engine_block", "vehicle_type"]
        self.df.drop(columns=drop_columns, inplace=True)
        self.df.dropna(inplace=True)
        numerics=["int8", "int16", "int32", "int64", "float16", "float32", "float64"]
        categorical_columns=[]
        features=self.df.columns.values.tolist()
        categorical_columns.extend(col for col in features if self.df[col].dtype not in numerics)
        for col in categorical_columns:
            if col in self.df.columns:
                le=LabelEncoder()
                self.df[col]=self.df[col].astype(str)
                le.fit(self.df[col])
                self.df[col]=le.transform(self.df[col])
                self.encoders[col]=le
        
        self.df=self.create_new_features(self.df)

    @staticmethod
    def create_new_features(data):
        current_year=2024
        data['miles_per_year']=(data['miles']/(current_year-data['year']).replace({0: 1})).round(0)
        data['age']=current_year-data['year']
        data.drop(columns=["year"], inplace=True)
        return data

    @staticmethod
    def log_transform(df, features):
        transformed_df=df.copy()
        for feature in features:
            transformed_df[feature]=np.log1p(transformed_df[feature].clip(lower=0))
        df[features]=transformed_df[features]
        return df

    def prepare_data(self):
        X=self.df.drop(columns=["price"])
        y=self.df["price"]
        return train_test_split(X, y, test_size=0.2, random_state=0)

class UsedCarPricePredictor:
    def __init__(self, data_handler):
        self.data_handler=data_handler
        self.X_train, self.X_test, self.y_train, self.y_test=self.data_handler.prepare_data()
        self.X_train=self.data_handler.log_transform(self.X_train, ['miles', 'miles_per_year'])
        self.X_test=self.data_handler.log_transform(self.X_test, ['miles', 'miles_per_year'])
        self.scaler=StandardScaler()
        self.X_train_scaled=self.scaler.fit_transform(self.X_train)
        self.X_test_scaled=self.scaler.transform(self.X_test)
        self.model=None

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
        self.calculate_additional_metrics()

    def acc_d(self, y_meas, y_pred):
        return mean_absolute_error(y_meas, y_pred)*len(y_meas)/sum(abs(y_meas))

    def acc_rmse(self, y_meas, y_pred):
        return (mean_squared_error(y_meas, y_pred))**0.5

    def calculate_additional_metrics(self):
        ytrain=self.model.predict(self.X_train_scaled)
        ytest=self.model.predict(self.X_test_scaled)
        acc_train_r2=[round(r2_score(self.y_train, ytrain)*100, 2)]
        acc_train_d=[round(self.acc_d(self.y_train, ytrain)*100, 2)]
        acc_train_rmse=[round(self.acc_rmse(self.y_train, ytrain)*100, 2)]
        acc_test_r2=[round(r2_score(self.y_test, ytest)*100, 2)]
        acc_test_d=[round(self.acc_d(self.y_test, ytest)*100, 2)]
        acc_test_rmse=[round(self.acc_rmse(self.y_test, ytest)*100, 2)]
        print(f"Train R2: {acc_train_r2[0]}")
        print(f"Train D: {acc_train_d[0]}")
        print(f"Train RMSE: {acc_train_rmse[0]}")
        print(f"Test R2: {acc_test_r2[0]}")
        print(f"Test D: {acc_test_d[0]}")
        print(f"Test RMSE: {acc_test_rmse[0]}")

    def predict(self, input_features):
        input_df=pd.DataFrame([input_features])
        input_df=self.data_handler.create_new_features(input_df)
        input_df=self.data_handler.log_transform(input_df, ['miles', 'miles_per_year'])
        numerics=["int8", "int16", "int32", "int64", "float16", "float32", "float64"]
        categorical_columns=[]
        features=input_df.columns.values.tolist()
        categorical_columns.extend(col for col in features if input_df[col].dtype not in numerics)
        for col in categorical_columns:
            if col in input_df.columns and col in self.data_handler.encoders:
                le=self.data_handler.encoders[col]
                input_df[col]=input_df[col].astype(str)
                input_df[col]=input_df[col].apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
        input_df=input_df[self.X_train.columns]
        input_scaled=self.scaler.transform(input_df)
        prediction=self.model.predict(input_scaled)
        return prediction[0]

if __name__=="__main__":
    data_handler=DataTransformation("vehicle_CA.csv")
    predictor=UsedCarPricePredictor(data_handler)
    predictor.optimize_model(n_trials=25)
    predictor.evaluate_model()
    while True:
        input_features={
            "year":int(input("Enter the Year: ")),
            "make":input("Enter the Make: "),
            "model":input("Enter the model: "),
            "body_type":input("Enter the Body Type: "),
            "drivetrain":input("Enter the Drivetrain: "),
            "transmission":input("Enter the Transmission: "),
            "fuel_type":input("Enter the Fuel Type: "),
            "miles":float(input("Enter the Miles: ")),
            "engine_size":input("Enter the Engine Size: "),
        }
        predicted_price=predictor.predict(input_features)
        print(f"The predicted used car price is: ${predicted_price:.2f}")
