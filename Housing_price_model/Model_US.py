import numpy as np
import pandas as pd
import optuna
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from xgboost import XGBRegressor
import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

class DataProcessor:
    def __init__(self, data_path):
        self.df=pd.read_csv(data_path)
        self.le_city=LabelEncoder()
        self.le_state=LabelEncoder()
        self.scalers={
            "house_size": StandardScaler(),
            "price": StandardScaler(),
            "bed": MinMaxScaler(),
            "bath": MinMaxScaler(),
            "acre_lot": MinMaxScaler()
        }
        self.preprocess()

    def preprocess(self):
        self.df.drop_duplicates(inplace=True)
        self.df["bed"].fillna(self.df["bed"].mode()[0], inplace=True)
        self.df["bath"].fillna(self.df["bath"].mode()[0], inplace=True)
        self.df["acre_lot"].fillna(self.df["acre_lot"].mode()[0], inplace=True)
        self.df["house_size"].fillna(self.df["house_size"].mode()[0], inplace=True)
        self.df=self.df.dropna(subset=["zip_code", "city"])
        self.df=self.df.drop("prev_sold_date", axis=1)
        column_num=["bed", "bath", "acre_lot", "house_size", "price"]
        Q1=self.df[column_num].quantile(0.25)
        Q3=self.df[column_num].quantile(0.75)
        IQR=Q3-Q1
        self.df=self.df[~((self.df[column_num]<(Q1-1.5*IQR))|(self.df[column_num]>(Q3+1.5*IQR))).any(axis=1)]
        for column in ["house_size", "bed", "bath", "acre_lot", "price"]:
            self.df[column]=self.scalers[column].fit_transform(self.df[column].values.reshape(len(self.df), 1))
        self.df["city"]=self.le_city.fit_transform(self.df["city"])
        self.df["state"]=self.le_state.fit_transform(self.df["state"])

    def get_train_test_data(self):
        X=self.df[["bed", "bath", "acre_lot", "zip_code", "house_size", "city", "state"]]
        y=self.df["price"]
        X=X[y.notna()]
        y=y[y.notna()]
        return train_test_split(X, y, test_size=0.2, random_state=42)
    
    def inverse_transform_price(self, price):
        return self.scalers["price"].inverse_transform(price.reshape(-1, 1))

class HousePricePredictor:
    def __init__(self, data_processor):
        self.data_processor=data_processor
        self.X_train, self.X_test, self.y_train, self.y_test=self.data_processor.get_train_test_data()
        print(self.X_train.head())
        self.model=None

    def objective(self, trial):
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
        }
        model=XGBRegressor(**param)
        model.fit(self.X_train, self.y_train)
        preds=model.predict(self.X_test)
        return np.sqrt(mean_squared_error(self.y_test, preds))

    def optimize_model(self, n_trials=5):
        study=optuna.create_study(direction="minimize")
        study.optimize(self.objective, n_trials=n_trials)
        best_params=study.best_trial.params
        self.model=XGBRegressor(**best_params)
        self.model.fit(self.X_train, self.y_train)
        print("Optimization complete. Best parameters:")
        for key, value in best_params.items():
            print(f" {key}: {value}")

    def evaluate_model(self):
        y_pred=self.model.predict(self.X_test)
        y_pred_inv=self.data_processor.inverse_transform_price(y_pred)
        y_test_inv=self.data_processor.inverse_transform_price(self.y_test.values)
        mse=mean_squared_error(y_test_inv, y_pred_inv)
        rmse=np.sqrt(mse)
        mae=mean_absolute_error(y_test_inv, y_pred_inv)
        r2=r2_score(y_test_inv, y_pred_inv)
        print(f"MAE: {mae}")
        print(f"MSE: {mse}")
        print(f"RMSE: {rmse}")
        print(f"R-squared: {r2}")

    def predict(self, input_features):
        input_df=pd.DataFrame([input_features])
        input_df["city"]=self.data_processor.le_city.transform(input_df["city"])
        input_df["state"]=self.data_processor.le_state.transform(input_df["state"])
        for column in ["house_size", "bed", "bath", "acre_lot"]:
            input_df[column]=self.data_processor.scalers[column].transform(input_df[column].values.reshape(len(input_df), 1))
        input_df=input_df[self.X_train.columns]
        input_scaled=input_df.values
        predicted_scaled=self.model.predict(input_scaled)
        return self.data_processor.inverse_transform_price(predicted_scaled)
if __name__=="__main__":
    data_path="estate_US.csv"
    data_processor=DataProcessor(data_path)
    predictor=HousePricePredictor(data_processor)
    predictor.optimize_model()
    predictor.evaluate_model()

    while True:
        user_input={
            "bed": float(input("Enter the number of bedrooms: ")),
            "bath": float(input("Enter the number of bathrooms: ")),
            "acre_lot": float(input("Enter the lot size in acres: ")),
            "zip_code": int(input("Enter the zip code: ")),
            "house_size": float(input("Enter the house size in square feet: ")),
            "city": input("Enter the city: "),
            "state": input("Enter the state: ")
        }
        predicted_price=predictor.predict(user_input)
        print(f"Predicted price: {predicted_price[0][0]:.3f}")
