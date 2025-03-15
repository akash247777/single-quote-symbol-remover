import streamlit as st
import pandas as pd
from io import BytesIO

def clean_invno_column(df, column_name="InvNo"):
    if column_name in df.columns:
        df[column_name] = df[column_name].astype(str).str.replace("'", "", regex=False)
    return df

st.title("CSV InvNo Cleaner")

uploaded_files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        df = pd.read_csv(file)
        df = clean_invno_column(df)
        
        csv_data = BytesIO()
        df.to_csv(csv_data, index=False)
        csv_data.seek(0)
        
        st.download_button(
            label=f"Download Cleaned {file.name}",
            data=csv_data,
            file_name=f"cleaned_{file.name}",
            mime="text/csv"
        )
