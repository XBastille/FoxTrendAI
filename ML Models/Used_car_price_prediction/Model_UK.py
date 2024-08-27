import numpy as np
import pandas as pd
import optuna
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,LabelEncoder,RobustScaler
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
from xgboost import XGBRegressor

class DataTransformation:
    def __init__(self,data_path):
        self.df=pd.read_csv(data_path)
        self.encoders={}
        self.scaler=StandardScaler()
        self.robust_scaler=RobustScaler()
        self.preprocess_data()

    def preprocess_data(self):
        self.df.drop(["Unnamed: 0","Service history"],axis=1,inplace=True)
        self.df.drop_duplicates(inplace=True)
        self.df.insert(1,"Brand",self.df.apply(lambda row: row["title"].split(" ")[0].upper(),axis=1))
        self.df.drop(columns=["title"],inplace=True)
        self.df.fillna({
            "Previous Owners": self.df["Previous Owners"].bfill(),
            "Engine": self.df["Engine"].mode()[0],
            "Doors": self.df["Doors"].median(),
            "Seats": self.df["Seats"].median(),
            "Emission Class": self.df["Emission Class"].mode()[0]
        },inplace=True)
        self.df=self.create_new_features(self.df)
        self.df=self.log_transform(self.df,["Mileage(miles)","Mileage_to_Engine_Ratio"])
        self.encode_features()
        self.scale_features()

    @staticmethod
    def create_new_features(data):
        current_year=2024
        data["age"]=current_year-data["Registration_Year"]
        data["Engine"]=data["Engine"].str.extract(r"(\d+\.\d+)").astype(float)
        data["Mileage_to_Engine_Ratio"]=data["Mileage(miles)"]/data["Engine"]
        return data

    @staticmethod
    def log_transform(df,features):
        transformed_df=df.copy()
        for feature in features:
            transformed_df[feature]=np.log1p(transformed_df[feature].clip(lower=0))
        df[features]=transformed_df[features]
        return df

    def encode_features(self):
        categorical_features=["Brand","Body type","Gearbox","Emission Class"]
        for col in categorical_features:
            if col in self.df.columns:
                le=LabelEncoder()
                self.df[col]=self.df[col].astype(str)
                le.fit(self.df[col])
                self.df[col]=le.transform(self.df[col])
                self.encoders[col]=le

    def scale_features(self):
        numerical_features=["Registration_Year","Engine","Mileage(miles)","age","Mileage_to_Engine_Ratio"]
        self.df[numerical_features]=self.robust_scaler.fit_transform(self.df[numerical_features])

    def prepare_data(self):
        col_to_take=["Registration_Year","Brand","Emission Class","age","Gearbox","Mileage(miles)","Engine","Body type","Mileage_to_Engine_Ratio"]
        X=self.df[col_to_take]
        y=self.df["Price"].values
        X_scaled=self.scaler.fit_transform(X)
        return train_test_split(X_scaled,y,test_size=0.2,random_state=42)

    def col(self):
        col_to_take=["Registration_Year","Brand","Emission Class","age","Gearbox","Mileage(miles)","Engine","Body type","Mileage_to_Engine_Ratio"]
        return self.df[col_to_take]

class UsedCarPricePredictor:
    def __init__(self,data_handler):
        self.data_handler=data_handler
        self.X_train,self.X_test,self.y_train,self.y_test=self.data_handler.prepare_data()
        self.X=self.data_handler.col()
        self.model=None

    def objective(self,trial):
        param={
            "objective": "reg:squarederror",
            "eval_metric": "rmse",
            "n_estimators": trial.suggest_int("n_estimators",100,1000),
            "max_depth": trial.suggest_int("max_depth",3,10),
            "learning_rate": trial.suggest_float("learning_rate",0.01,0.1),
            "subsample": trial.suggest_float("subsample",0.6,1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree",0.6,1.0),
            "reg_alpha": trial.suggest_float("reg_alpha",0,10),
            "reg_lambda": trial.suggest_float("reg_lambda",0,10),
            "verbosity": 0,
        }
        model=XGBRegressor(**param)
        model.fit(self.X_train,self.y_train)
        preds=model.predict(self.X_test)
        return np.sqrt(mean_squared_error(self.y_test,preds))

    def optimize_model(self,n_trials=25):
        study=optuna.create_study(direction="minimize")
        study.optimize(self.objective,n_trials=n_trials)
        best_params=study.best_trial.params
        self.model=XGBRegressor(**best_params)
        self.model.fit(self.X_train,self.y_train)
        print("Optimization complete. Best parameters:")
        for key,value in best_params.items():
            print(f"{key}: {value}")

    def evaluate_model(self):
        predictions=self.model.predict(self.X_test)
        mae=mean_absolute_error(self.y_test,predictions)
        mse=mean_squared_error(self.y_test,predictions)
        rmse=np.sqrt(mse)
        r2=r2_score(self.y_test,predictions)
        print(f"MAE on test data: {mae}")
        print(f"MSE on test data: {mse}")
        print(f"RMSE on test data: {rmse}")
        print(f"R-squared value on test data: {r2}")

    def prepare_input(self,input_features):
        input_df=pd.DataFrame([input_features])
        input_df=self.data_handler.create_new_features(input_df)
        input_df=self.data_handler.log_transform(input_df,["Mileage(miles)","Mileage_to_Engine_Ratio"])
        for col in input_df.columns:
            if col in self.data_handler.encoders:
                le=self.data_handler.encoders[col]
                input_df[col]=input_df[col].astype(str).apply(lambda x: le.transform([x])[0] if x in le.classes_ else -1)
        input_df=input_df[self.X.columns]
        numerical_features=["Registration_Year","Engine","Mileage(miles)","age","Mileage_to_Engine_Ratio"]
        input_df[numerical_features]=self.data_handler.robust_scaler.transform(input_df[numerical_features])
        return self.data_handler.scaler.transform(input_df)

    def predict(self,input_features):
        input_prepared=self.prepare_input(input_features)
        prediction=self.model.predict(input_prepared)
        return prediction[0]

if __name__=="__main__":
    data_handler=DataTransformation("used_cars_UK.csv")
    predictor=UsedCarPricePredictor(data_handler)
    predictor.optimize_model(n_trials=25)
    predictor.evaluate_model()
    while True:
        input_features={
            "Registration_Year": int(input("Enter the Registration Year: ")),
            "Brand": input("Enter the Brand: "),
            "Emission Class": input("Enter the Emission Class: (e.g., '')"),
            "Gearbox": input("Enter the Gearbox: "),
            "Mileage(miles)": float(input("Enter the Mileage (in miles): ")),
            "Engine": input("Enter the Engine (e.g., '2.0L'): "),
            "Body type": input("Enter the Body Type: ")
        }
        predicted_price=predictor.predict(input_features)
        print(f"The predicted used car price is: €{predicted_price:.2f}")
