import pandas as pd
import numpy as np
import optuna
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import MinMaxScaler
from imblearn.combine import SMOTETomek
from xgboost import XGBClassifier
import warnings
pd.set_option("display.max_columns", None)
pd.options.display.float_format="{:,.2f}".format
warnings.filterwarnings("ignore")
class LoanApprovalModel:
    def __init__(self, data_path):
        self.df=pd.read_csv(data_path)
        self.preprocess_data()
        self.X_train, self.X_test, self.y_train, self.y_test=self.split_data()
        self.scaler=MinMaxScaler()
        self.X_train=self.scaler.fit_transform(self.X_train)
        self.X_test=self.scaler.transform(self.X_test)
        self.X_train, self.y_train = self.balance_data(self.X_train, self.y_train)
        self.model=None

    def preprocess_data(self):
        self.df.drop(columns="Applicant_ID", inplace=True)
        self.df=self.df.drop(columns=["Residence_City", "Residence_State", "Occupation", "Years_in_Current_Residence"]).copy()
        self.df.columns=["Annual_Income", "Applicant_Age", "Work_Experience", "Marital_Status", "House_Ownership", "Vehicle_Ownership", "Years_in_Current_Work", "Loan_Default_Risk"]
        self.df=pd.get_dummies(self.df, columns=["Marital_Status", "House_Ownership", "Vehicle_Ownership"], drop_first=True)*1

    def split_data(self):
        X=self.df.drop(columns=["Loan_Default_Risk"])
        y=self.df["Loan_Default_Risk"]
        return train_test_split(X, y, test_size=0.2, random_state=79)

    def balance_data(self, X, y):
        smote_tomek=SMOTETomek(random_state=79)
        return smote_tomek.fit_resample(X, y)

    def objective(self, trial):
        param={
            "objective": "binary:logistic",
            "learning_rate": trial.suggest_float("learning_rate", 0.001, 0.3, log=True),
            "max_depth": trial.suggest_int("max_depth", 3, 15),
            "gamma": trial.suggest_float("gamma", 0, 1.0),
            "min_child_weight": trial.suggest_int("min_child_weight", 1, 7),
            "subsample": trial.suggest_float("subsample", 0.5, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.4, 1.0)
        }
        model=XGBClassifier(**param)
        kf=KFold(n_splits=5, shuffle=True, random_state=42)
        scores=cross_val_score(model, self.X_train, self.y_train, cv=kf, scoring="roc_auc")
        return scores.mean()

    def optimize_model(self, n_trials=50):
        study=optuna.create_study(direction="maximize")
        study.optimize(self.objective, n_trials=n_trials)
        self.best_params=study.best_params
        print("Best parameters:")
        for key, value in self.best_params.items():
            print(f"{key}: {value}")
        self.model=XGBClassifier(**self.best_params)
        self.model.fit(self.X_train, self.y_train)

    def evaluate_model(self):
        train_score=self.model.score(self.X_train, self.y_train)*100
        print(f"TRAIN SCORE: {train_score:.2f}%")
        predictions=self.model.predict(self.X_test)
        test_score=accuracy_score(self.y_test, predictions)*100
        print(f"TEST SCORE: {test_score:.2f}%")
        kf=KFold(n_splits=10, shuffle=True, random_state=42)
        scores=cross_val_score(self.model, self.df.drop(columns=["Loan_Default_Risk"]), self.df["Loan_Default_Risk"], cv=kf, scoring="roc_auc")
        print(f"CROSS VALIDATION SCORE: {np.mean(scores)*100:.2f}%")

    def predict(self, input_features):
        input_df=pd.DataFrame([input_features])
        input_df=pd.get_dummies(input_df, columns=["Marital_Status", "House_Ownership", "Vehicle_Ownership"], drop_first=True)*1
        Marital_Status_col=f"Marital_Status_{input_features['Marital_Status']}"
        House_Ownership_col=f"House_Ownership_{input_features['House_Ownership']}"
        Vehicle_Ownership_col=f"Vehicle_Ownership_{input_features['Vehicle_Ownership']}"
        cols=["Annual_Income", "Applicant_Age", "Work_Experience", "Years_in_Current_Work", "Marital_Status_single", "House_Ownership_owned", "House_Ownership_rented", "Vehicle_Ownership_yes"]
        for col in cols:
            if col not in input_df.columns:
                input_df[col]=1 if col in [Marital_Status_col, House_Ownership_col, Vehicle_Ownership_col] else 0
        input_df=input_df[cols]
        input_scaled=self.scaler.transform(input_df)
        prediction=self.model.predict(input_scaled)
        return prediction[0]

if __name__=="__main__":
    loan_model=LoanApprovalModel("Applicant-details.csv")
    loan_model.optimize_model(n_trials=25)
    loan_model.evaluate_model()
    while True:
        input_features={
            "Annual_Income": float(input("Enter the Annual Income: ")),
            "Applicant_Age": int(input("Enter the Applicant Age: ")),
            "Work_Experience": int(input("Enter the Work Experience: ")),
            "Years_in_Current_Work": int(input("Enter the Years in Current Work: ")),
            "Marital_Status": input("Enter the Marital Status (single/married): "),
            "House_Ownership": input("Enter the House Ownership (owned/rented/nan): "),
            "Vehicle_Ownership": input("Enter the Vehicle Ownership (yes/no): ")
        }
        prediction=loan_model.predict(input_features)
        result="Approved" if prediction==0 else "Denied"
        print(f"The loan application is {result}")
