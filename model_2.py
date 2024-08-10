# model_2.py
import datetime
import numpy as np
import optuna
import pandas as pd
import sys
#import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from main import StockDataVisualizer
import warnings
warnings.filterwarnings("ignore")

class StockPredictor:
    def __init__(self, company_name, num_days_pred, stock_data):
        self.company_name=company_name
        self.num_days_pred=num_days_pred
        self.stock_data=stock_data
        self.df_xgb=self.prepare_data()

    def mean_absolute_percentage_error(self, y_true, y_pred):
        y_true, y_pred=np.array(y_true), np.array(y_pred)
        return np.mean(np.abs((y_true-y_pred)/y_true))*100

    def add_lags(self, df):
        target="Close"
        for i in range(1, 13):
            df[f"lag{i}"]=df[target].shift(self.num_days_pred*i)
        return df

    def create_features(self, df):
        df=df.copy()
        df["hour"]=df.index.hour
        df["dayofweek"]=df.index.dayofweek
        df["quarter"]=df.index.quarter
        df["month"]=df.index.month
        df["year"]=df.index.year
        df["dayofyear"]=df.index.dayofyear
        df["dayofmonth"]=df.index.day
        df["weekofyear"]=df.index.isocalendar().week
        return df

    def prepare_data(self):
        df=self.stock_data.copy()
        df=self.create_features(df)
        df=self.add_lags(df)
        df.dropna(inplace=True)
        return df

    def split_data(self):
        X=self.df_xgb.drop(columns="Close")
        y=self.df_xgb["Close"]
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def optimize_model(self, X_train, y_train, X_test, y_test):
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
            model.fit(X_train, y_train)
            y_pred=model.predict(X_test)
            return np.sqrt(mean_squared_error(y_test, y_pred))
        
        study=optuna.create_study(direction="minimize")
        study.optimize(objective, n_trials=2)
        best_params=study.best_trial.params
        print("Best parameters found by Optuna:")
        #for key, value in best_params.items():
        #    print(f"{key}: {value}")
        return best_params

    def train_best_model(self, X_train, y_train, best_params):
        model=XGBRegressor(**best_params)
        model.fit(X_train, y_train)
        return model

    def predict(self, model, X_test, y_test):
        y_pred=model.predict(X_test)
        rmse=np.sqrt(mean_squared_error(y_test, y_pred))
        r2=r2_score(y_test, y_pred)
        mape=self.mean_absolute_percentage_error(y_test, y_pred)
        return y_pred, rmse, r2, mape

    def predict_future(self, model):
        start=self.df_xgb.index.max()
        end=start+pd.Timedelta(days=self.num_days_pred)
        future=pd.date_range(start=start, end=end, freq="1d")
        future_df=pd.DataFrame(index=future)
        future_df["isFuture"]=True
        self.df_xgb["isFuture"]=False
        df_and_future=pd.concat([self.df_xgb, future_df])
        df_and_future=self.create_features(df_and_future)
        df_and_future=self.add_lags(df_and_future)
        print(df_and_future.head())
        future_w_features=df_and_future.query("isFuture").copy()
        future_w_features["pred"]=model.predict(future_w_features.drop(columns=["Close", "isFuture"]))
        prediction_xgb=pd.DataFrame(future_w_features["pred"])
        prediction_xgb.index.name="Date"
        '''plt.figure(figsize=(10, 6))
        plt.plot(prediction_xgb.index, prediction_xgb["pred"], color="green", label="Predicted Future Values")
        plt.title(f"Predicted Future Values for {self.company_name} (Next {self.num_days_pred} days)")
        plt.xlabel("Date")
        plt.ylabel("Stock Price")
        plt.legend()
        plt.show()'''
        return prediction_xgb

    def calculate_percentage_change(self, predictions):
        initial_price=predictions.iloc[0]
        final_price=predictions.iloc[-1]
        return ((final_price-initial_price)/initial_price)*100

    def run(self):
        X_train, X_test, y_train, y_test=self.split_data()
        best_params=self.optimize_model(X_train, y_train, X_test, y_test)
        best_model=self.train_best_model(X_train, y_train, best_params)
        y_pred, rmse, r2, mape=self.predict(best_model, X_test, y_test)
        #print(f"RMSE: {rmse}")
        #print(f"R² Score: {r2}")
        #print(f"Mean Absolute Percentage Error: {mape}%")
        future_predictions=self.predict_future(best_model)
        X=future_predictions.index.strftime('%Y-%m-%d').tolist() 
        Y=future_predictions["pred"].tolist()
        print(X)
        print(Y)
        percentage_change=self.calculate_percentage_change(future_predictions["pred"])
        '''print(f"Predicted Future Prices:\n{future_predictions}")
        print(f"Predicted percentage change over the next {self.num_days_pred} days: {percentage_change:.2f}%")
        if percentage_change>0:
            print("The model predicts an upward trend. It might be a good time to buy.")
        else:
            print("The model predicts a downward trend. It might be better to wait.")'''

if __name__=="__main__":
    if len(sys.argv)<3:
        sys.exit(1)
    company_name=sys.argv[1]
    num_days_pred=int(sys.argv[2])
    data=StockDataVisualizer(company_name)
    predictor=StockPredictor(company_name, num_days_pred, data.download_stock_data())
    predictor.run()