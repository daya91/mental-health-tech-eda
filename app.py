import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Mental Health in Tech", layout="wide")

st.title("Mental Health in Tech Workplace")
st.write("Exploratory Data Analysis Dashboard")

url = "https://raw.githubusercontent.com/techtenant/OSMI-Mental-Health-in-Tech-Survey/master/survey.csv"
df = pd.read_csv(url)

df["Age"] = pd.to_numeric(df["Age"], errors="coerce")
df = df[(df["Age"] >= 15) & (df["Age"] <= 80)]

df["Gender"] = df["Gender"].astype(str).str.lower().str.strip()

def clean_gender(x):
    if x in ["male", "m", "man"]:
        return "Male"
    elif x in ["female", "f", "woman"]:
        return "Female"
    return "Other"

df["Gender"] = df["Gender"].apply(clean_gender)

st.sidebar.header("Filters")

gender = st.sidebar.multiselect(
    "Select Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

filtered_df = df[df["Gender"].isin(gender)]

col1, col2, col3 = st.columns(3)
col1.metric("Total Respondents", len(filtered_df))
col2.metric("Treatment Yes", (filtered_df["treatment"] == "Yes").sum())
col3.metric("Average Age", round(filtered_df["Age"].mean(), 1))

st.subheader("Treatment Status")
fig, ax = plt.subplots()
sns.countplot(data=filtered_df, x="treatment", ax=ax)
st.pyplot(fig)

st.subheader("Family History vs Treatment")
fig, ax = plt.subplots()
sns.countplot(data=filtered_df, x="family_history", hue="treatment", ax=ax)
st.pyplot(fig)

st.subheader("Mental Health Benefits")
fig, ax = plt.subplots()
sns.countplot(data=filtered_df, x="benefits", ax=ax)
st.pyplot(fig)

st.subheader("Conclusion")
st.write(
    "The dashboard highlights treatment patterns, the relationship between "
    "family history and treatment, and the availability of employer mental "
    "health benefits."
)
