import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import StandardScaler
import optuna
from xgboost import XGBRegressor

import warnings
warnings.filterwarnings("ignore")

class HousePricePredictor:
    def __init__(self,csv_file):
        self.df=pd.read_csv(csv_file)
        self.preprocess_data()
        
    def preprocess_data(self):
        columns_with_meaningfull_null=["PoolQC","MiscFeature","Alley","Fence","FireplaceQu","GarageCond","GarageType",
            "GarageFinish","GarageQual","BsmtFinType2","BsmtExposure","BsmtQual","BsmtFinType1",
            "BsmtCond","MasVnrType"]
        for column in columns_with_meaningfull_null:
            self.df[column].fillna("None",inplace=True)
        columns_with_not_meaningfull_null=["GarageYrBlt","MasVnrArea"]
        for column in columns_with_not_meaningfull_null:
            self.df[column].fillna(self.df[column].median(),inplace=True)
        self.df.drop(columns=["LotFrontage"],inplace=True)
        self.df.dropna(inplace=True)
        self.numeric_features=[
            'MSSubClass','LotArea','OverallQual','OverallCond','YearBuilt',
            'YearRemodAdd','MasVnrArea','BsmtFinSF1','BsmtFinSF2','BsmtUnfSF',
            'TotalBsmtSF','1stFlrSF','2ndFlrSF','LowQualFinSF','GrLivArea',
            'BsmtFullBath','BsmtHalfBath','FullBath','HalfBath','BedroomAbvGr',
            'KitchenAbvGr','TotRmsAbvGrd','Fireplaces','GarageYrBlt',
            'GarageCars','GarageArea','WoodDeckSF','OpenPorchSF',
            'EnclosedPorch','3SsnPorch','ScreenPorch','PoolArea','MiscVal'
        ]
        self.categorical_features=[
            'MSZoning','Street','Alley','LotShape','LandContour','Utilities',
            'LotConfig','LandSlope','Neighborhood','Condition1','Condition2',
            'BldgType','HouseStyle','RoofStyle','RoofMatl','Exterior1st',
            'Exterior2nd','MasVnrType','ExterQual','ExterCond','Foundation',
            'BsmtQual','BsmtCond','BsmtExposure','BsmtFinType1','BsmtFinType2',
            'Heating','HeatingQC','CentralAir','Electrical','KitchenQual',
            'Functional','FireplaceQu','GarageType','GarageFinish','GarageQual',
            'GarageCond','PavedDrive','PoolQC','Fence','MiscFeature',
            'SaleType','SaleCondition'
        ]
        
    def display_feature_selection(self,features,feature_type,selected_features):
        print(f"\nAvailable {feature_type} features:")
        for i,feature in enumerate(features,1):
            if feature not in selected_features:
                print(f"{i}. {feature}")
        print(f"\nSelected {feature_type} features: {selected_features}")

    def select_features(self,features,feature_type):
        selected_features=[]
        while True:
            self.display_feature_selection(features,feature_type,selected_features)
            choice=int(input(f"Select a {feature_type} feature to add (1-{len(features)}), or 0 to finish: "))
            if choice==0:
                break
            elif 1<=choice<=len(features):
                selected_feature=features[choice-1]
                if selected_feature not in selected_features:
                    selected_features.append(selected_feature)
                    print(f"Added feature: {selected_feature}")
                else:
                    print(f"Feature {selected_feature} already selected.")
            else:
                print(f"Invalid choice. Please select a number between 1 and {len(features)}.")
        return selected_features
    
    def fit(self):
        self.selected_numeric_features=self.select_features(self.numeric_features,"numeric")
        self.selected_categorical_features=self.select_features(self.categorical_features,"categorical")
        df1=self.df[self.selected_numeric_features+["SalePrice"]]
        df2=self.df[self.selected_categorical_features]
        dummies=pd.get_dummies(df2,drop_first=True)
        self.df_processed=pd.concat([df1,dummies],axis=1)
        self.scaler=StandardScaler()
        cols=list(self.df_processed.columns.values)
        cols.remove("SalePrice")
        self.df_processed[cols]=self.scaler.fit_transform(self.df_processed[cols])
        X=self.df_processed.drop(["SalePrice"],axis=1).values
        y=self.df_processed["SalePrice"].values
        self.X_train,self.X_test,self.y_train,self.y_test=train_test_split(X,y,train_size=0.7,test_size=0.3,random_state=42)
        self.optimize_model()
        
    def optimize_model(self):
        def objective(trial):
            param={
                'objective': 'reg: squarederror',
                'n_estimators': trial.suggest_int('n_estimators',100,1000),
                'max_depth': trial.suggest_int('max_depth',3,10),
                'learning_rate': trial.suggest_float('learning_rate',0.01,0.3),
                'subsample': trial.suggest_float('subsample',0.5,1.0),
                'colsample_bytree': trial.suggest_float('colsample_bytree',0.5,1.0),
                'reg_alpha': trial.suggest_float('reg_alpha',0,10),
                'reg_lambda': trial.suggest_float('reg_lambda',0,10),
            }
            model=XGBRegressor(**param)
            model.fit(self.X_train,self.y_train)
            preds=model.predict(self.X_test)
            return np.sqrt(mean_squared_error(self.y_test,preds))
        
        study=optuna.create_study(direction='minimize')
        study.optimize(objective,n_trials=25)
        self.best_params=study.best_trial.params
        self.model=XGBRegressor(**self.best_params)
        self.model.fit(self.X_train,self.y_train)
        y_pred_xgb_train=self.model.predict(self.X_train)
        print('Train R2 Square : ',round(r2_score(self.y_train,y_pred_xgb_train),9))
        y_pred_xgb_test=self.model.predict(self.X_test)
        print('Test R2 Square : ',round(r2_score(self.y_test,y_pred_xgb_test),9))
        print("Best parameters found by Optuna:")
        print(self.best_params)
    
    def predict(self):
        while True:
            print("Please enter values for the selected features:")
            input_data={
                feature:input(f"{feature}: ")
                for feature in self.selected_numeric_features
                +self.selected_categorical_features
            }
            input_df=pd.DataFrame([input_data])
            for feature in self.selected_numeric_features:
                input_df[feature]=pd.to_numeric(input_df[feature])
            dummies=pd.get_dummies(input_df[self.selected_categorical_features],drop_first=True)
            input_df=pd.concat([input_df[self.selected_numeric_features],dummies],axis=1)
            for col in self.df_processed.columns:
                if col not in input_df.columns and col!="SalePrice":
                    input_df[col]=0
            input_df=input_df[self.df_processed.columns.drop("SalePrice")]
            input_df=self.scaler.transform(input_df)
            prediction=self.model.predict(input_df)
            print(f"Predicted Sale Price: {prediction[0]}")
            
    def display_feature_descriptions(self):
        feature_descriptions={
            'MSSubClass': 'Identifies the type of dwelling involved in the sale.',
            'LotArea': 'Lot size in square feet.',
            'OverallQual': 'Rates the overall material and finish of the house.',
            'OverallCond': 'Rates the overall condition of the house.',
            'YearBuilt': 'Original construction date.',
            'YearRemodAdd': 'Remodel date (same as construction date if no remodeling or additions).',
            'MasVnrArea': 'Masonry veneer area in square feet.',
            'BsmtFinSF1': 'Type 1 finished square feet.',
            'BsmtFinSF2': 'Type 2 finished square feet.',
            'BsmtUnfSF': 'Unfinished square feet of basement area.',
            'TotalBsmtSF': 'Total square feet of basement area.',
            '1stFlrSF': 'First floor square feet.',
            '2ndFlrSF': 'Second floor square feet.',
            'LowQualFinSF': 'Low quality finished square feet (all floors).',
            'GrLivArea': 'Above grade (ground) living area square feet.',
            'BsmtFullBath': 'Basement full bathrooms.',
            'BsmtHalfBath': 'Basement half bathrooms.',
            'FullBath': 'Full bathrooms above grade.',
            'HalfBath': 'Half baths above grade.',
            'BedroomAbvGr': 'Number of bedrooms above basement level.',
            'KitchenAbvGr': 'Number of kitchens.',
            'TotRmsAbvGrd': 'Total rooms above grade (does not include bathrooms).',
            'Fireplaces': 'Number of fireplaces.',
            'GarageYrBlt': 'Year garage was built.',
            'GarageCars': 'Size of garage in car capacity.',
            'GarageArea': 'Size of garage in square feet.',
            'WoodDeckSF': 'Wood deck area in square feet.',
            'OpenPorchSF': 'Open porch area in square feet.',
            'EnclosedPorch': 'Enclosed porch area in square feet.',
            '3SsnPorch': 'Three season porch area in square feet.',
            'ScreenPorch': 'Screen porch area in square feet.',
            'PoolArea': 'Pool area in square feet.',
            'MiscVal': 'Value of miscellaneous feature.',
            'MSZoning': 'Identifies the general zoning classification of the sale.',
            'Street': 'Type of road access to property.',
            'Alley': 'Type of alley access to property.',
            'LotShape': 'General shape of property.',
            'LandContour': 'Flatness of the property.',
            'Utilities': 'Type of utilities available.',
            'LotConfig': 'Lot configuration.',
            'LandSlope': 'Slope of property.',
            'Neighborhood': 'Physical locations within Ames city limits.',
            'Condition1': 'Proximity to various conditions.',
            'Condition2': 'Proximity to various conditions (if more than one is present).',
            'BldgType': 'Type of dwelling.',
            'HouseStyle': 'Style of dwelling.',
            'RoofStyle': 'Type of roof.',
            'RoofMatl': 'Roof material.',
            'Exterior1st': 'Exterior covering on house.',
            'Exterior2nd': 'Exterior covering on house (if more than one material).',
            'MasVnrType': 'Masonry veneer type.',
            'ExterQual': 'Evaluates the quality of the material on the exterior.',
            'ExterCond': 'Evaluates the present condition of the material on the exterior.',
            'Foundation': 'Type of foundation.',
            'BsmtQual': 'Evaluates the height of the basement.',
            'BsmtCond': 'Evaluates the general condition of the basement.',
            'BsmtExposure': 'Refers to walkout or garden level walls.',
            'BsmtFinType1': 'Rating of basement finished area.',
            'BsmtFinType2': 'Rating of basement finished area (if multiple types).',
            'Heating': 'Type of heating.',
            'HeatingQC': 'Heating quality and condition.',
            'CentralAir': 'Central air conditioning.',
            'Electrical': 'Electrical system.',
            'KitchenQual': 'Kitchen quality.',
            'Functional': 'Home functionality rating.',
            'FireplaceQu': 'Fireplace quality.',
            'GarageType': 'Garage location.',
            'GarageFinish': 'Interior finish of the garage.',
            'GarageQual': 'Garage quality.',
            'GarageCond': 'Garage condition.',
            'PavedDrive': 'Paved driveway.',
            'PoolQC': 'Pool quality.',
            'Fence': 'Fence quality.',
            'MiscFeature': 'Miscellaneous feature not covered in other categories.',
            'SaleType': 'Type of sale.',
            'SaleCondition': 'Condition of sale.'
        }
        print("\nFeature Descriptions:")
        for feature,description in feature_descriptions.items():
            print(f"{feature}: {description}")

if __name__=="__main__":
    predictor=HousePricePredictor("estate_AUS.csv")
    predictor.fit()
    predictor.display_feature_descriptions()
    predictor.predict()
