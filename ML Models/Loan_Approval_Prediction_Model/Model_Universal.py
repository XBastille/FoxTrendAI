import numpy as np
import pandas as pd
import warnings
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score
import optuna
from xgboost import XGBClassifier

warnings.filterwarnings('ignore')

class LoanApprovalModel:
    def __init__(self,csv_file):
        self.df=pd.read_csv(csv_file)
        self.preprocess_data()

    def preprocess_data(self):
        self.df.drop(['ID','ZIP.Code'],axis=1,inplace=True)
        self.df['Experience']=abs(self.df['Experience'])
        self.df.drop_duplicates(inplace=True)
        self.df['Income']=np.cbrt(self.df['Income'])
        self.df['CCAvg']=np.cbrt(self.df['CCAvg'])
        self.df['Mortgage']=np.sqrt(self.df['Mortgage'])
        for col in ['CCAvg','Mortgage']:
            lower_limit,upper_limit=self.replace_outlier(self.df[col])
            self.df[col]=np.where(self.df[col]<lower_limit,lower_limit,self.df[col])
            self.df[col]=np.where(self.df[col]>upper_limit,upper_limit,self.df[col])
        self.scale_features()

    def replace_outlier(self,col):
        Q1,Q3=col.quantile([0.25,0.75])
        IQR=Q3-Q1
        lower_range=Q1-(1.5*IQR)
        upper_range=Q3+(1.5*IQR)
        return lower_range,upper_range

    def scale_features(self):
        self.scaler=StandardScaler()
        self.df_scaled=self.df.copy()
        self.X=self.df_scaled.drop(['Personal.Loan','Securities.Account','Online'],axis=1)
        self.Y=self.df_scaled['Personal.Loan']
        self.split_and_oversample_data()

    def split_and_oversample_data(self):
        self.X_train,self.X_test,self.y_train,self.y_test=train_test_split(self.X,self.Y,test_size=0.4,random_state=42)
        smote=SMOTE(random_state=42)
        self.X_train_upsampled,self.y_train_upsampled=smote.fit_resample(self.X_train,self.y_train)
        self.optimize_model()

    def optimize_model(self):
        def objective(trial):
            param={
                'objective':'binary:logistic',
                'max_depth':trial.suggest_int('max_depth',3,10),
                'learning_rate':trial.suggest_float('learning_rate',0.01,0.3),
                'n_estimators':trial.suggest_int('n_estimators',100,500),
                'subsample':trial.suggest_float('subsample',0.5,1.0),
                'colsample_bytree':trial.suggest_float('colsample_bytree',0.5,1.0),
                'reg_alpha':trial.suggest_float('reg_alpha',0,10),
                'reg_lambda':trial.suggest_float('reg_lambda',0,10),
            }
            xgb_model=XGBClassifier(**param)
            xgb_model.fit(self.X_train_upsampled,self.y_train_upsampled)
            preds=xgb_model.predict(self.X_test)
            return accuracy_score(self.y_test,preds)

        study=optuna.create_study(direction='maximize')
        study.optimize(objective,n_trials=25)
        self.best_params=study.best_trial.params
        print("Best parameters found by Optuna:")
        print(self.best_params)
        self.train_best_model()

    def train_best_model(self):
        self.model=XGBClassifier(**self.best_params)
        self.model.fit(self.X_train_upsampled,self.y_train_upsampled)
        self.evaluate_model()

    def evaluate_model(self):
        y_pred_train_xgb=self.model.predict(self.X_train_upsampled)
        y_pred_test_xgb=self.model.predict(self.X_test)
        train_accuracy=accuracy_score(self.y_train_upsampled,y_pred_train_xgb)
        print("XGBoost Training Accuracy:",round(train_accuracy,3)*100)
        test_accuracy=accuracy_score(self.y_test,y_pred_test_xgb)
        print("XGBoost Testing Accuracy:",round(test_accuracy,3)*100)

    def predict(self):
        while True:
            print("Please enter values for the following features:")
            input_data={
                'Age': float(input("Age: ")),
                'Experience': float(input("Experience: ")),
                'Income': float(input("Income: ")),
                'Family': float(input("Family: ")),
                'CCAvg': float(input("CCAvg: ")),
                'Education': float(input("Education: ")),
                'Mortgage': float(input("Mortgage: ")),
                'CD.Account': int(input("CD.Account (0 or 1): ")),
                'CreditCard': int(input("CreditCard (0 or 1): ")),
            }
            input_df=pd.DataFrame([input_data])
            input_df['Income']=np.cbrt(input_df['Income'])
            input_df['CCAvg']=np.cbrt(input_df['CCAvg'])
            input_df['Mortgage']=np.sqrt(input_df['Mortgage'])
            for col in ['CCAvg','Mortgage']:
                lower_limit,upper_limit=self.replace_outlier(self.df[col])
                input_df[col]=np.where(input_df[col]<lower_limit,lower_limit,input_df[col])
                input_df[col]=np.where(input_df[col]>upper_limit,upper_limit,input_df[col])
            input_df_scaled=input_df.copy()
            prediction=self.model.predict(input_df_scaled)
            print(f"Predicted Personal Loan Approval: {prediction[0]}")

if __name__=='__main__':
    model=LoanApprovalModel("bankloan.csv")
    model.predict()
