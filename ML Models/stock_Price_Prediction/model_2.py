import datetime
import numpy as np
import optuna
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import warnings
import requests
import mlflow
import mlflow.xgboost
import logging
from xgboost import XGBRegressor
from main import StockDataVisualizer
from mlflow.tracking import MlflowClient
from transformers import pipeline, BertTokenizer, BertForSequenceClassification
from sklearn.metrics import mean_squared_error, r2_score
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StockPredictor:
    def __init__(self, company_name, num_days_pred, no_of_trial, stock_data):
        self.company_name=company_name
        mlflow.set_experiment(f"Stock_Prediction_{company_name}_{num_days_pred}")
        self.num_days_pred=num_days_pred
        self.no_of_trial=no_of_trial
        self.stock_data=stock_data
        self.df_xgb=self.prepare_data()
        logger.info(f"Initializing StockPredictor for {company_name} with {num_days_pred} days prediction")

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
        ma_windows=[self.num_days_pred, 2*self.num_days_pred]
        for window in ma_windows:
            df[f"MA{window}"]=df["Close"].rolling(window=window).mean()
        df["volatility"]=df["Close"].rolling(window=self.num_days_pred).std()
        df["EMA"]=df["Close"].ewm(span=self.num_days_pred, adjust=False).mean()
        df["momentum"]=df["Close"]-df["Close"].shift(self.num_days_pred//2)
        df["sentiment"]=self.get_sentiment_score()
        return df

    def get_sentiment_score(self):
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        url=f"https://finance.yahoo.com/quote/{self.company_name}/news?p={self.company_name}"
        r=requests.get(url, headers=headers)
        soup=BeautifulSoup(r.text, "lxml")
        headlines=[headline.text for headline in soup.find_all("h3", class_="clamp yf-1044anq")]
        tokenizer=BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')
        model=BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone')
        sentiment_analyzer=pipeline('sentiment-analysis', model=model, tokenizer=tokenizer, return_all_scores=True)
        sentiment_scores=[]
        ticker=yf.Ticker(self.company_name)
        company_info=ticker.info
        company_name=company_info.get('longName', 'Name not available')
        for headline in headlines:
            if self.company_name in headline or company_name.split()[0].lower() in headline.lower():
                print(headline)
                sentiment=sentiment_analyzer(headline)
                compound_score=sentiment[0][1]['score']-sentiment[0][2]['score']  
                sentiment_scores.append(compound_score)
        print(sentiment_scores)
        return np.mean(sentiment_scores) if sentiment_scores else 0

    def prepare_data(self):
        df=self.stock_data.copy()
        df=self.create_features(df)
        df=self.add_lags(df)
        df.dropna(inplace=True)
        return df

    def split_data(self):
        df_train=self.df_xgb.iloc[:-self.num_days_pred]
        df_test=self.df_xgb.iloc[-self.num_days_pred:]
        X_train=df_train.drop(columns="Close")
        y_train=df_train["Close"]
        X_test=df_test.drop(columns="Close")
        y_test=df_test["Close"]
        return X_train, X_test, y_train, y_test

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
        study.optimize(objective, n_trials=self.no_of_trial)
        best_params=study.best_trial.params
        for param_name, param_value in best_params.items():
            mlflow.log_param(param_name, param_value)
        print("Best parameters found by Optuna:")
        for key, value in best_params.items():
            print(f"{key}: {value}")
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
        future_w_features=df_and_future.query("isFuture").copy()
        future_w_features["pred"]=model.predict(future_w_features.drop(columns=["Close", "isFuture"]))
        prediction_xgb=pd.DataFrame(future_w_features["pred"])
        plt.figure(figsize=(10, 6))
        plt.plot(prediction_xgb.index, prediction_xgb["pred"], color="green", label="Predicted Future Values")
        plt.title(f"Predicted Future Values for {self.company_name} (Next {self.num_days_pred} days)")
        plt.xlabel("Date")
        plt.ylabel("Stock Price")
        plt.legend()
        plt.show()
        return prediction_xgb

    def calculate_percentage_change(self, predictions):
        initial_price=predictions.iloc[0]
        final_price=predictions.iloc[-1]
        return ((final_price-initial_price)/initial_price)*100

    def run(self):
        client = MlflowClient()
        with mlflow.start_run():
            X_train, X_test, y_train, y_test=self.split_data()
            best_params=self.optimize_model(X_train, y_train, X_test, y_test)
            best_model=self.train_best_model(X_train, y_train, best_params)
            y_pred, rmse, r2, mape=self.predict(best_model, X_test, y_test)
            print(f"RMSE: {rmse}")
            print(f"R² Score: {r2}")
            print(f"Mean Absolute Percentage Error: {mape}%")
            future_predictions=self.predict_future(best_model)
            mlflow.log_param("company_name", self.company_name)
            mlflow.log_param("num_days_pred", self.num_days_pred)
            mlflow.log_param("no_of_trial", self.no_of_trial)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("r2", r2)
            mlflow.log_metric("mape", mape)
            model_name = f"{self.company_name}_{self.num_days_pred}_stock_predictor"
            mlflow.xgboost.log_model(best_model, "xgboost_model", registered_model_name=model_name)
            model_version = client.get_latest_versions(model_name, stages=["None"])[0].version            
            client.transition_model_version_stage(
                name=model_name,
                version=model_version,
                stage="Staging"
            )
            percentage_change=self.calculate_percentage_change(future_predictions["pred"])
            print(f"Predicted Future Prices:\n{future_predictions}")
            print(f"Predicted percentage change over the next {self.num_days_pred} days: {percentage_change:.2f}%")
            if percentage_change>0:
                print("The model predicts an upward trend. It might be a good time to buy.")
            else:
                print("The model predicts a downward trend. It might be better to wait.")
            print(f"Model {model_name} version {model_version} has been registered and transitioned to Staging.")

if __name__=="__main__":
    logger.info("Starting prediction run")
    company_name=input("Enter the company ticker (e.g., TSLA): ")
    num_days_pred=int(input("Enter the number of days to predict into the future: "))
    no_of_trial=int(input("Enter the no. of trial (NOTE:- The more the no. of trials,  the better the result will be, but more time): "))
    data=StockDataVisualizer(company_name)
    predictor=StockPredictor(company_name, num_days_pred, no_of_trial, data.stock_data)
    predictor.run()