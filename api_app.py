"""essential modules"""

from fastapi import FastAPI
import joblib
import pandas as pd
import sqlite3
import logging
import os
from pydantic import BaseModel
import datetime

# fast api initial
app = FastAPI()
# load the model
model = joblib.load("Model/loan_model.joblib")


# log initialize and formate of the logs
logging.basicConfig(filename="logs.txt", filemode="a", format="%(asctime)s %(message)s")
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@app.on_event("startup")
def start_evbents() -> None:
    init_db()


# database connection
def get_connection() -> sqlite3.Connection:
    return sqlite3.connect("/loans.db", check_same_thread=False)


# creation fodata base
def init_db() -> None:
    conn = get_connection()
    cursor = conn.cursor()
    logger.info("table creation")
    cursor.execute("""CREATE TABLE IF NOT EXISTS applications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        person_age INTEGER,
                        person_income FLOAT,
                        person_emp_exp INTEGER,
                        loan_amnt FLOAT,
                        loan_int_rate FLOAT,
                        loan_percent_income FLOAT,
                        cb_person_cred_hist_length INTEGER,
                        credit_score INTEGER,
                        person_gender_female INTEGER,
                        person_gender_male INTEGER,
                        person_education_Associate INTEGER,
                        person_education_Bachelor INTEGER,
                        person_education_Doctorate INTEGER,
                        person_education_HighSchool INTEGER,
                        person_education_Master INTEGER,
                        person_home_ownership_MORTGAGE INTEGER,
                        person_home_ownership_OTHER INTEGER,
                        person_home_ownership_OWN INTEGER,
                        person_home_ownership_RENT INTEGER,
                        loan_intent_DEBTCONSOLIDATION INTEGER,
                        loan_intent_EDUCATION INTEGER,
                        loan_intent_HOMEIMPROVEMENT INTEGER,
                        loan_intent_MEDICAL INTEGER,
                        loan_intent_PERSONAL INTEGER,
                        loan_intent_VENTURE INTEGER,
                        previous_loan_defaults_on_file_No INTEGER,
                        previous_loan_defaults_on_file_Yes INTEGER,
                        prediction INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )""")
    logger.info("db is created")
    conn.commit()
    conn.close()
    logger.info("crate db connection close")


# insert the values
def insert_values(data) -> None:
    logger.info("insert the values to the local database")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO applications (
                        person_age, person_income, person_emp_exp, loan_amnt, loan_int_rate,
                        loan_percent_income, cb_person_cred_hist_length, credit_score,
                        person_gender_female, person_gender_male,
                        person_education_Associate, person_education_Bachelor, person_education_Doctorate,
                        person_education_HighSchool, person_education_Master,
                        person_home_ownership_MORTGAGE, person_home_ownership_OTHER, person_home_ownership_OWN,
                        person_home_ownership_RENT,
                        loan_intent_DEBTCONSOLIDATION, loan_intent_EDUCATION, loan_intent_HOMEIMPROVEMENT,
                        loan_intent_MEDICAL, loan_intent_PERSONAL, loan_intent_VENTURE,
                        previous_loan_defaults_on_file_No, previous_loan_defaults_on_file_Yes,
                        prediction, created_at
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        data,
    )
    logger.info("values inserted")
    conn.commit()
    conn.close()
    logger.info("connection closed in the insert functiopn")


# bsaeclass for sapi
class Loanpara(BaseModel):
    person_age: int
    person_income: float
    person_emp_exp: int
    loan_amnt: float
    loan_int_rate: float
    loan_percent_income: float
    cb_person_cred_hist_length: int
    credit_score: int
    person_gender_female: int
    person_gender_male: int
    person_education_Associate: int
    person_education_Bachelor: int
    person_education_Doctorate: int
    person_education_HighSchool: int
    person_education_Master: int
    person_home_ownership_MORTGAGE: int
    person_home_ownership_OTHER: int
    person_home_ownership_OWN: int
    person_home_ownership_RENT: int
    loan_intent_DEBTCONSOLIDATION: int
    loan_intent_EDUCATION: int
    loan_intent_HOMEIMPROVEMENT: int
    loan_intent_MEDICAL: int
    loan_intent_PERSONAL: int
    loan_intent_VENTURE: int
    previous_loan_defaults_on_file_No: int
    previous_loan_defaults_on_file_Yes: int


# for the prediction
@app.post("/api/v1/predict")
def predict(app_data: Loanpara) -> str:
    dict_data = app_data.dict()
    df = pd.DataFrame([dict_data])
    prediction = model.predict(df)[0]
    logger.info(f"the predictied values is {prediction}")
    insert_values(list(dict_data.values()) + [prediction] + [datetime.datetime.now()])
    return f"prediction : {prediction}"
