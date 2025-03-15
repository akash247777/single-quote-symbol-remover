import streamlit as st
import pandas as pd
from io import BytesIO
import zipfile
import concurrent.futures

def clean_invno_column(df, column_name="InvNo"):
    if column_name in df.columns:
        df[column_name] = df[column_name].astype(str).str.replace("'", "", regex=False)
    return df

def process_file(file):
    df = pd.read_csv(file)
    df = clean_invno_column(df)
    output = BytesIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return file.name, output.getvalue()

st.title("CSV InvNo Cleaner")

uploaded_files = st.file_uploader("Upload CSV files", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(process_file, uploaded_files)
            for filename, data in results:
                zip_file.writestr(f"cleaned_{filename}", data)
    
    zip_buffer.seek(0)
    st.download_button(
        label="Download All Cleaned Files",
        data=zip_buffer,
        file_name="cleaned_files.zip",
        mime="application/zip"
    )
