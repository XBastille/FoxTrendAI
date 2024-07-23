import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import average_precision_score
from xgboost import XGBClassifier
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class FraudDetectionModel:
    def __init__(self, data_path, random_state=5):
        self.data_path = data_path
        self.random_state = random_state
        self.model = None
        self.X = None
        self.Y = None
        self.trainX = None
        self.testX = None
        self.trainY = None
        self.testY = None
        self.weights = None
        self.load_data()

    def load_data(self):
        df = pd.read_csv(self.data_path)
        df = df.rename(columns={"oldbalanceOrg":"oldBalanceOrig", "newbalanceOrig":"newBalanceOrig", 
                                "oldbalanceDest":"oldBalanceDest", "newbalanceDest":"newBalanceDest"})
        self.X = df.loc[(df.type == "TRANSFER") | (df.type == "CASH_OUT")]
        self.Y = self.X["isFraud"]
        del self.X["isFraud"]
        self.X = self.X.drop(["nameOrig", "nameDest", "isFlaggedFraud"], axis=1)
        self.X=pd.get_dummies(self.X, columns=["type"], drop_first=True)
        Xfraud = self.X.loc[self.Y == 1]
        XnonFraud = self.X.loc[self.Y == 0]
        fraud_fraction = len(Xfraud.loc[(Xfraud.oldBalanceDest == 0) & 
                                        (Xfraud.newBalanceDest == 0) & 
                                        (Xfraud.amount != 0)]) / (1.0 * len(Xfraud))
        non_fraud_fraction = len(XnonFraud.loc[(XnonFraud.oldBalanceDest == 0) & 
                                               (XnonFraud.newBalanceDest == 0) & 
                                               (XnonFraud.amount != 0)]) / (1.0 * len(XnonFraud))
       self.X.loc[(self.X.oldBalanceDest == 0) & (self.X.newBalanceDest == 0) & (self.X.amount != 0), 
                    ["oldBalanceDest", "newBalanceDest"]] = -1
        self.X.loc[(self.X.oldBalanceOrig == 0) & (self.X.newBalanceOrig == 0) & (self.X.amount != 0), 
                    ["oldBalanceOrig", "newBalanceOrig"]] = np.nan
        self.X["errorBalanceOrig"] = self.X.newBalanceOrig + self.X.amount - self.X.oldBalanceOrig
        self.X["errorBalanceDest"] = self.X.oldBalanceDest + self.X.amount - self.X.newBalanceDest
        self.X.head().to_csv("model_trial.csv")
        self.trainX, self.testX, self.trainY, self.testY = train_test_split(self.X, self.Y, test_size=0.2, random_state=self.random_state)
        self.weights = (self.Y == 0).sum() / (1.0 * (self.Y == 1).sum())

    def train_model(self):
        self.model = XGBClassifier(max_depth=10, scale_pos_weight=self.weights, n_estimators=308, learning_rate=0.07064544702456911, n_jobs=4)
        self.model.fit(self.trainX, self.trainY)
        probabilities = self.model.predict_proba(self.testX)
        auprc = average_precision_score(self.testY, probabilities[:, 1])
        print(f"AUPRC = {auprc}")

    def predict(self, input_data):
        input_df = pd.DataFrame([input_data], columns=self.X.columns)
        if input_data["type"] in ["TRANSFER", "CASH_OUT"]:
            input_df["type_TRANSFER"] = np.where(input_data["type"] == "TRANSFER", 1, 0)
        input_df["errorBalanceOrig"] = input_df.newBalanceOrig + input_df.amount - input_df.oldBalanceOrig
        input_df["errorBalanceDest"] = input_df.oldBalanceDest + input_df.amount - input_df.newBalanceDest
        input_df.to_csv("input_trial.csv")
        return self.model.predict(input_df)

def main():
    data_path = "PS_20174392719_1491204439457_log.csv"
    model = FraudDetectionModel(data_path)
    model.train_model()
    while True:
        step = int(input("Enter step: "))
        payment_type = input("Enter type (TRANSFER/CASH_OUT/PAYMENT/CASH_IN/DEBIT): ")
        amount = float(input("Enter amount: "))
        oldBalanceOrig = float(input("Enter oldBalanceOrig: "))
        newBalanceOrig = float(input("Enter newBalanceOrig: "))
        oldBalanceDest = float(input("Enter oldBalanceDest: "))
        newBalanceDest = float(input("Enter newBalanceDest: "))
        input_data = {
            "step": step,
            "type": payment_type,
            "amount": amount,
            "oldBalanceOrig": oldBalanceOrig,
            "newBalanceOrig": newBalanceOrig,
            "oldBalanceDest": oldBalanceDest,
            "newBalanceDest": newBalanceDest,
        }
        prediction = model.predict(input_data)
        print(f"The predicted class for the input transaction is: {prediction[0]}")

if __name__=="__main__":
    main()
