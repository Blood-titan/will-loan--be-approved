import streamlit as st
import pandas as pd
import sklearn
import joblib
import sqlite3
import datetime


def init_db():
    conn = sqlite3.connect("loans.db")
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()


def insert_application(data):
    conn = sqlite3.connect("loans.db")
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
    conn.commit()
    conn.close()


st.title("will your loan be approved?")

init_db()
# Personal Information
st.header("Personal Information")
person_age = st.number_input("Age", min_value=18, max_value=100, value=30)
person_income = st.number_input("Annual Income", min_value=0, value=50000)
person_emp_exp = st.number_input("Years of Employment", min_value=0, value=5)

# Loan Information
st.header("Loan Information")
loan_amnt = st.number_input("Loan Amount", min_value=1000, value=10000)
loan_int_rate = st.number_input(
    "Loan Interest Rate (%)", min_value=0.0, max_value=100.0, value=5.0
)
loan_percent_income = st.number_input(
    "Loan as % of Income", min_value=0.0, max_value=100.0, value=20.0
)
cb_person_cred_hist_length = st.number_input(
    "Credit History Length (months)", min_value=0, value=60
)
credit_score = st.number_input("Credit Score", min_value=300, max_value=850, value=700)

# Gender
st.header("Gender")
gender = st.selectbox("Select Gender", ["Female", "Male"])
person_gender_female = 1 if gender == "Female" else 0
person_gender_male = 1 if gender == "Male" else 0

# Education
st.header("Education")
education = st.selectbox(
    "Education Level", ["High School", "Associate", "Bachelor", "Master", "Doctorate"]
)
person_education_Associate = 1 if education == "Associate" else 0
person_education_Bachelor = 1 if education == "Bachelor" else 0
person_education_Doctorate = 1 if education == "Doctorate" else 0
person_education_High_School = 1 if education == "High School" else 0
person_education_Master = 1 if education == "Master" else 0

# Home Ownership
st.header("Home Ownership")
home_ownership = st.selectbox("Home Ownership", ["MORTGAGE", "OTHER", "OWN", "RENT"])
person_home_ownership_MORTGAGE = 1 if home_ownership == "MORTGAGE" else 0
person_home_ownership_OTHER = 1 if home_ownership == "OTHER" else 0
person_home_ownership_OWN = 1 if home_ownership == "OWN" else 0
person_home_ownership_RENT = 1 if home_ownership == "RENT" else 0

# Loan Intent
st.header("Loan Intent")
loan_intent = st.selectbox(
    "Loan Purpose",
    [
        "DEBTCONSOLIDATION",
        "EDUCATION",
        "HOMEIMPROVEMENT",
        "MEDICAL",
        "PERSONAL",
        "VENTURE",
    ],
)
loan_intent_DEBTCONSOLIDATION = 1 if loan_intent == "DEBTCONSOLIDATION" else 0
loan_intent_EDUCATION = 1 if loan_intent == "EDUCATION" else 0
loan_intent_HOMEIMPROVEMENT = 1 if loan_intent == "HOMEIMPROVEMENT" else 0
loan_intent_MEDICAL = 1 if loan_intent == "MEDICAL" else 0
loan_intent_PERSONAL = 1 if loan_intent == "PERSONAL" else 0
loan_intent_VENTURE = 1 if loan_intent == "VENTURE" else 0

# Previous Loan Defaults
st.header("Previous Loan Defaults")
previous_defaults = st.selectbox("Previous Defaults?", ["No", "Yes"])
previous_loan_defaults_on_file_No = 1 if previous_defaults == "No" else 0
previous_loan_defaults_on_file_Yes = 1 if previous_defaults == "Yes" else 0

# Submit Button
if st.button("Submit"):
    input_data = pd.DataFrame(
        {
            "person_age": [person_age],
            "person_income": [person_income],
            "person_emp_exp": [person_emp_exp],
            "loan_amnt": [loan_amnt],
            "loan_int_rate": [loan_int_rate],
            "loan_percent_income": [loan_percent_income],
            "cb_person_cred_hist_length": [cb_person_cred_hist_length],
            "credit_score": [credit_score],
            "person_gender_female": [person_gender_female],
            "person_gender_male": [person_gender_male],
            "person_education_Associate": [person_education_Associate],
            "person_education_Bachelor": [person_education_Bachelor],
            "person_education_Doctorate": [person_education_Doctorate],
            "person_education_High School": [person_education_High_School],
            "person_education_Master": [person_education_Master],
            "person_home_ownership_MORTGAGE": [person_home_ownership_MORTGAGE],
            "person_home_ownership_OTHER": [person_home_ownership_OTHER],
            "person_home_ownership_OWN": [person_home_ownership_OWN],
            "person_home_ownership_RENT": [person_home_ownership_RENT],
            "loan_intent_DEBTCONSOLIDATION": [loan_intent_DEBTCONSOLIDATION],
            "loan_intent_EDUCATION": [loan_intent_EDUCATION],
            "loan_intent_HOMEIMPROVEMENT": [loan_intent_HOMEIMPROVEMENT],
            "loan_intent_MEDICAL": [loan_intent_MEDICAL],
            "loan_intent_PERSONAL": [loan_intent_PERSONAL],
            "loan_intent_VENTURE": [loan_intent_VENTURE],
            "previous_loan_defaults_on_file_No": [previous_loan_defaults_on_file_No],
            "previous_loan_defaults_on_file_Yes": [previous_loan_defaults_on_file_Yes],
        }
    )

    st.write("Input Data:")
    st.dataframe(input_data)
    model = joblib.load("model/loan_model.joblib")
    prediction = model.predict(input_data)

    st.write("Prediction Result:")
    if prediction[0] == 1:
        st.success("Loan Approved")
    else:
        st.error("Loan Denied")
    insert_application(
        (
            person_age,
            person_income,
            person_emp_exp,
            loan_amnt,
            loan_int_rate,
            loan_percent_income,
            cb_person_cred_hist_length,
            credit_score,
            person_gender_female,
            person_gender_male,
            person_education_Associate,
            person_education_Bachelor,
            person_education_Doctorate,
            person_education_High_School,
            person_education_Master,
            person_home_ownership_MORTGAGE,
            person_home_ownership_OTHER,
            person_home_ownership_OWN,
            person_home_ownership_RENT,
            loan_intent_DEBTCONSOLIDATION,
            loan_intent_EDUCATION,
            loan_intent_HOMEIMPROVEMENT,
            loan_intent_MEDICAL,
            loan_intent_PERSONAL,
            loan_intent_VENTURE,
            previous_loan_defaults_on_file_No,
            previous_loan_defaults_on_file_Yes,
            int(prediction[0]),
            datetime.datetime.now(),
        )
    )
