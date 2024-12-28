import os
import sys
from dataclasses import dataclass
from src.utils import evaluate_models,save_object

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging


@dataclass
class ModelTrainerConfig():
    model_trainer_file_path=os.path.join('artifact','model.pkl')


class ModelTrainer():
    def __init__(self):
        self.model_trainer_config=ModelTrainerConfig()
    
    def initiate_model_trainer(self,train_arr,test_arr):
        try:
            logging.info("splitting training and testing data")
            X_test,y_test,X_train,y_train=(
                test_arr[:,:-1],
                test_arr[:,-1],
                train_arr[:,:-1],
                train_arr[:,-1]
            )

            models={
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor()
            }


            model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,
                                             models=models)
            
            best_model_score=max(sorted(model_report.values()))
            best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]
           

            best_model = models[best_model_name]

            print(best_model)

            if best_model_score<0.6:
                raise CustomException("No Best Model Found")
            
            logging.info(f"Best model found on training and testing data")

            save_object(
                file_path=self.model_trainer_config.model_trainer_file_path,
                obj=best_model
            )
            
            predicted=best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)
            return r2_square


        except Exception as e:
            raise CustomException(e,sys)

            
 
    