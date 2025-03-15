import streamlit as st
import pandas as pd
from io import BytesIO

def clean_invno_column(df, column_name="InvNo"):
    if column_name in df.columns:
        df[column_name] = df[column_name].astype(str).str.replace("'", "", regex=False)
    return df

def process_files(uploaded_files):
    cleaned_dfs = []
    for file in uploaded_files:
        df = pd.read_csv(file)
        df = clean_invno_column(df)
        cleaned_dfs.append(df)
    
    if cleaned_dfs:
        final_df = pd.concat(cleaned_dfs, ignore_index=True)
        return final_df
    return None

def convert_df_to_csv(df):
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output

st.title("CSV InvNo Cleaner")

uploaded_files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    cleaned_df = process_files(uploaded_files)
    if cleaned_df is not None:
        csv_data = convert_df_to_csv(cleaned_df)
        st.download_button(
            label="Download Cleaned CSV",
            data=csv_data,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )
