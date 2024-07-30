import numpy as np
import pandas as pd
import optuna
from sklearn.preprocessing import LabelEncoder,StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score,mean_absolute_percentage_error
from xgboost import XGBRegressor
import warnings
import sys

if not sys.warnoptions:
    warnings.simplefilter("ignore")

class DataTransformation:
    def __init__(self,data_path):
        self.df=pd.read_csv(data_path)
        self.encoders={}
        self.preprocess_data()

    def preprocess_data(self):
        self.df=self.df.drop(['Title','ColourExtInt','Model','Car/Suv'],axis=1)
        self.df['FuelConsumption']=self.df['FuelConsumption'].str.split('/').str[0].str.split().str[0]
        self.df['Location']=self.df['Location'].str.split(',').str[1].str.strip()
        self.df['Engine']=self.df['Engine'].str.split(',').str[1].str.split().str[0]
        self.df['CylindersinEngine']=self.df['CylindersinEngine'].str.split().str[0]
        self.df['Doors']=self.df['Doors'].str.split().str[0]
        self.df['Seats']=self.df['Seats'].str.split().str[0]
        self.df.replace(['-','POA'],np.NAN,inplace=True)
        self.df.dropna(subset=['Location','BodyType','Price','Transmission','FuelType','Kilometres'],inplace=True)
        self.df['Engine'].fillna(self.df[~self.df['Engine'].isnull()]['Engine'].str.strip().astype(float).mode()[0],inplace=True)
        self.df['FuelConsumption'].fillna(self.df[~self.df['FuelConsumption'].isnull()]['FuelConsumption'].str.strip().astype(float).mode()[0],inplace=True)
        self.df['CylindersinEngine'].fillna(self.df[~self.df['CylindersinEngine'].isnull()]['CylindersinEngine'].str.strip().astype(int).mode()[0],inplace=True)
        self.df['Doors'].fillna(self.df[~self.df['Doors'].isnull()]['Doors'].str.strip().astype(int).mode()[0],inplace=True)
        self.df['Seats'].fillna(self.df[~self.df['Seats'].isnull()]['Seats'].str.strip().astype(int).mode()[0],inplace=True)
        self.df['Engine']=self.df['Engine'].astype(float)
        self.df['FuelConsumption']=self.df['FuelConsumption'].astype(float)
        self.df['Kilometres']=self.df['Kilometres'].astype(float)
        self.df['CylindersinEngine']=self.df['CylindersinEngine'].astype(int)
        self.df['Doors']=self.df['Doors'].astype(int)
        self.df['Seats']=self.df['Seats'].astype(int)
        self.df['Price']=self.df['Price'].astype(float)
        self.df=self.df.drop(15313)
        self.label_encode_columns()
        self.one_hot_encode_columns()
        self.remove_outliers()
        
    def label_encode_columns(self):
        LE=LabelEncoder()
        self.df['Brand']=LE.fit_transform(self.df['Brand'])
        self.encoders['Brand']=LE
        
    def one_hot_encode_columns(self):
        df_get_dummies=['UsedOrNew','Transmission','DriveType','FuelType','BodyType']
        for col in df_get_dummies:
            onehotcoding=pd.get_dummies(self.df[col],prefix=col).astype(int)
            self.df=pd.concat([self.df,onehotcoding],axis=1)
        self.df.drop(['UsedOrNew','Transmission','DriveType','FuelType','BodyType','Location'],axis=1,inplace=True)
    
    def remove_outliers(self):
        def outlier(a):
            Q1=a.quantile(0.25)
            Q3=a.quantile(0.75)
            IQR=Q3-Q1
            L=Q1-1.5*IQR
            U=Q3+1.5*IQR
            return (L,U)

        self.df=self.df.loc[self.df['Year']>=outlier(self.df['Year'])[0]]
        self.df=self.df.loc[self.df['Year']<=outlier(self.df['Year'])[1]]
        self.df=self.df.loc[self.df['Engine']>=outlier(self.df['Engine'])[0]]
        self.df=self.df.loc[self.df['Engine']<=outlier(self.df['Engine'])[1]]
        self.df=self.df.loc[self.df['FuelConsumption']>=outlier(self.df['FuelConsumption'])[0]]
        self.df=self.df.loc[self.df['FuelConsumption']<=outlier(self.df['FuelConsumption'])[1]]
        self.df=self.df.loc[self.df['Price']>=outlier(self.df['Price'])[0]]
        self.df=self.df.loc[self.df['Price']<=outlier(self.df['Price'])[1]]
        self.df=self.df.loc[self.df['Kilometres']>=outlier(self.df['Kilometres'])[0]]
        self.df=self.df.loc[self.df['Kilometres']<=outlier(self.df['Kilometres'])[1]]
    
    def prepare_data(self):
        y=self.df['Price']
        x=self.df.drop(['Price'],axis=1)
        return train_test_split(x,y,test_size=0.2,random_state=42)

class VehiclePricePredictor:
    def __init__(self,data_handler):
        self.data_handler=data_handler
        self.X_train,self.X_test,self.y_train,self.y_test=self.data_handler.prepare_data()
        self.X_train.head().to_csv("data_trial.csv")
        self.scaler=StandardScaler()
        self.X_train_scaled=self.scaler.fit_transform(self.X_train)
        self.X_test_scaled=self.scaler.transform(self.X_test)
        self.model=None

    def objective(self,trial):
        param={
            "objective":"reg:squarederror",
            "eval_metric":"rmse",
            "n_estimators":trial.suggest_int("n_estimators",100,1000),
            "max_depth":trial.suggest_int("max_depth",3,10),
            "learning_rate":trial.suggest_float("learning_rate",0.01,0.1),
            "subsample":trial.suggest_float("subsample",0.6,1.0),
            "colsample_bytree":trial.suggest_float("colsample_bytree",0.6,1.0),
            "reg_alpha":trial.suggest_float("reg_alpha",0,10),
            "reg_lambda":trial.suggest_float("reg_lambda",0,10),
            "verbosity":0
        }
        model=XGBRegressor(**param)
        model.fit(self.X_train_scaled,self.y_train)
        preds=model.predict(self.X_test_scaled)
        return np.sqrt(mean_squared_error(self.y_test,preds))

    def optimize_model(self,n_trials=25):
        study=optuna.create_study(direction="minimize")
        study.optimize(self.objective,n_trials=n_trials)
        best_params=study.best_trial.params
        self.model=XGBRegressor(**best_params)
        self.model.fit(self.X_train_scaled,self.y_train)
        print("Optimization complete. Best parameters:")
        for key,value in best_params.items():
            print(f"{key}:{value}")

    def evaluate_model(self):
        y_pred=self.model.predict(self.X_test_scaled)
        mae=mean_absolute_error(self.y_test,y_pred)
        mse=mean_squared_error(self.y_test,y_pred)
        rmse=np.sqrt(mse)
        r2=r2_score(self.y_test,y_pred)
        mape=mean_absolute_percentage_error(self.y_test,y_pred)
        print(f"MAE: {mae}")
        print(f"MSE: {mse}")
        print(f"RMSE: {rmse}")
        print(f"R-squared:{r2}")
        print(f"MAPE: {mape}")

    def predict(self,input_features):
        input_df=pd.DataFrame([input_features])
        LE=self.data_handler.encoders['Brand']
        input_df['Brand']=LE.transform(input_df['Brand'])
        df_get_dummies=['UsedOrNew','Transmission','DriveType','FuelType','BodyType']
        for col in df_get_dummies:
            onehotcoding=pd.get_dummies(input_df[col],prefix=col).astype(int)
            input_df=pd.concat([input_df,onehotcoding],axis=1)
        brand_col=f"Brand_{input_features['Brand']}"
        transmission_col=f"Transmission_{input_features['Transmission']}"
        drive_type_col=f"DriveType_{input_features['DriveType']}"
        fuel_type_col=f"FuelType_{input_features['FuelType']}"
        body_type_col=f"BodyType_{input_features['BodyType']}"
        for col in self.X_train.columns:
            if col not in input_df.columns:
                input_df[col]=1 if col in [brand_col,transmission_col,drive_type_col,fuel_type_col,body_type_col] else 0
        input_df=input_df[self.X_train.columns]
        input_df.to_csv("input_trial.csv")
        input_scaled=self.scaler.transform(input_df)
        return self.model.predict(input_scaled)

if __name__=="__main__":
    data_path='vehicle_AUS.csv'
    data_handler=DataTransformation(data_path)
    predictor=VehiclePricePredictor(data_handler)
    predictor.optimize_model()
    predictor.evaluate_model()
    while True:
        user_input={
            "Brand": input("Enter the Brand: "),
            "Year": int(input("Enter the Year: ")),
            "Engine": float(input("Enter the Engine size: ")),
            "FuelConsumption": float(input("Enter the FuelConsumption: ")),
            "Kilometres": float(input("Enter the Kilometres: ")),
            "CylindersinEngine": int(input("Enter the number of Cylinders in Engine: ")),
            "Doors": int(input("Enter the number of Doors: ")),
            "Seats": int(input("Enter the number of Seats: ")),
            "Transmission": input("Enter the Transmission type: "),
            "DriveType": input("Enter the Drive type: "),
            "FuelType": input("Enter the Fuel type: "),
            "BodyType": input("Enter the Body type: "),
            "UsedOrNew": "USED"
        }
        prediction=predictor.predict(user_input)
        print(f"The predicted price of the vehicle is: {prediction}")

