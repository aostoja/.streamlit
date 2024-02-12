import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.sidebar.header('Parameters')

def main():
    st.title('Streamlit App - Upload Dataset')

    uploaded_file = st.file_uploader('Upload a CSV file', type = ['csv'])

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file, encoding = 'latin1')

        st.dataframe(df.head(3))

        select_col_1 = st.sidebar.selectbox('Select Column #1', df.columns)
        select_col_2 = st.sidebar.selectbox('Select Column #2', df.columns)
        select_col_3 = st.sidebar.selectbox('Select Column #3', df.columns)

        col1, col2, col3 = st.columns(3)
        col1.metric(select_col_1 +' Mean Value', round(df[select_col_1].mean()))
        col2.metric(select_col_2 +' Maximum Value', df[select_col_2].max())
        col3.metric(select_col_3 +' Minimum Value', df[select_col_3].min())

        st.markdown("Column #1 Counts Bar Chart")
        st.bar_chart(df[select_col_1].value_counts())

        st.markdown("Column #2 Line Chart")
        st.line_chart(df[select_col_2])

if __name__ == '__main__':
    main()

