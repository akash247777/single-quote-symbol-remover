import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile

def clean_invno_column(df, column_name="InvNo"):
    if column_name in df.columns:
        df[column_name] = df[column_name].astype(str).str.replace("'", "", regex=False)
    return df

def process_files(uploaded_files):
    cleaned_files = {}
    for file in uploaded_files:
        df = pd.read_csv(file)
        df = clean_invno_column(df)
        
        csv_data = BytesIO()
        df.to_csv(csv_data, index=False)
        csv_data.seek(0)
        
        cleaned_files[f"cleaned_{file.name}"] = csv_data.getvalue()
    return cleaned_files

st.title("CSV InvNo Cleaner")

uploaded_files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    cleaned_files = process_files(uploaded_files)
    
    if cleaned_files:
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for filename, data in cleaned_files.items():
                zip_file.writestr(filename, data)
        zip_buffer.seek(0)
        
        st.download_button(
            label="Download All Cleaned Files",
            data=zip_buffer,
            file_name="cleaned_files.zip",
            mime="application/zip"
        )
