import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_icon=":bar_chart:",layout="wide")
st.title('Streamlit Dashboard - Upload Dataset')
st.sidebar.header('Parameters')

def main():
    #st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader('Upload a file', type = (['csv', 'xlsx']))

    if uploaded_file is not None:

        df = pd.read_csv(uploaded_file, encoding = 'latin1')

        st.dataframe(df.head(5))

        col1, col2 = st.columns((2))
        potential_datetime_columns = []
        for column_name in df.columns:
            try:
                pd.to_datetime(df[column_name], errors='raise')
                potential_datetime_columns.append(column_name)
            except (TypeError, ValueError):
                pass
        if len(potential_datetime_columns) == 1:
            df[potential_datetime_columns] = pd.to_datetime(df[potential_datetime_columns])
            startDate = pd.to_datetime(df[potential_datetime_columns]).min()
            endDate = pd.to_datetime(df[potential_datetime_columns]).max()

            with col1:
                date1 = pd.to_datetime(st.date_input("Start Date", startDate))

            with col2:
                date2 = pd.to_datetime(st.date_input("End Date", endDate))

            df = df[(df[potential_datetime_columns] >= date1) & (df[potential_datetime_columns] <= date2)].copy()
        elif len(potential_datetime_columns) == 0:
            pass
        else:
            potential_datetime_columns.append(None)
            selected_datetime_col = st.selectbox('Select Date Column:', potential_datetime_columns)
            if selected_datetime_col is not None:
                df[selected_datetime_col] = pd.to_datetime(df[selected_datetime_col])
                startDate = pd.to_datetime(df[selected_datetime_col]).min()
                endDate = pd.to_datetime(df[selected_datetime_col]).max()

                with col1:
                    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

                with col2:
                    date2 = pd.to_datetime(st.date_input("End Date", endDate))
                df = df[(df[selected_datetime_col] >= date1) & (df[selected_datetime_col] <= date2)].copy()
            else:
                pass
        st.sidebar.header("Choose your filter: ")
        # Region
        region1_select = st.sidebar.selectbox("Pick a Primary Data Filter", df.columns.unique())
        region1 = st.sidebar.multiselect("Pick a " + str(region1_select), df[region1_select].unique())
        if not region1:
            df2 = df.copy()
        else:
            df2 = df[df[region1_select].isin(region1)]
        # State
        region2_select = st.sidebar.selectbox("Pick a Secondary Data Filter", df2.columns.unique())
        region2 = st.sidebar.multiselect("Pick a " + str(region2_select), df2[region2_select].unique())
        if not region2:
            df3 = df2.copy()
        else:
            df3 = df2[df2[region2_select].isin(region2)]

        if not region1 and not region2:
            filtered_df = df
        elif not region2:
            filtered_df = df[df[region1_select].isin(region1)]
        elif not region1:
            filtered_df = df[df[region2_select].isin(region2)]
        elif region2:
            filtered_df = df3[df[region2_select].isin(region2)]
        elif region1:
            filtered_df = df3[df[region1_select].isin(region1)]
        elif region1 and region2:
            filtered_df = df3[df[region1_select].isin(region1) & df3[region2_select].isin(region2)]
        else:
            filtered_df = df3[df3[region1_select].isin(region1) & df3[region2_select].isin(region2)]

        select_col_1 = st.sidebar.selectbox('Select Column #1', df.columns)
        select_col_2 = st.sidebar.selectbox('Select Column #2', df.columns)
        select_col_3 = st.sidebar.selectbox('Select Column #3', df.columns)

        col1, col2, col3 = st.columns(3)
        col1.metric(select_col_1 +' Mean Value', np.round(df[select_col_1].mean()))
        col2.metric(select_col_2 +' Maximum Value', df[select_col_2].max())
        col3.metric(select_col_3 +' Minimum Value', df[select_col_3].min())

        with col1:
            category_df_xaxis = st.selectbox('Select Category', df.columns)
        with col2:
            category_df_yaxis = st.selectbox('Select Quantity Column', df.columns)
        with col3:
            category_df_y2axis = st.selectbox('Select Region', df.columns)
        category_df = filtered_df.groupby(by = [category_df_xaxis], as_index = False)[category_df_yaxis].sum()

        cl1, cl2 = st.columns(2)
        with cl1:
            st.subheader(str(category_df_yaxis) + ' vs. ' + str(category_df_xaxis))
            fig = px.bar(category_df, x = str(category_df_xaxis), y = str(category_df_yaxis), text = ['${:,.2f}'.format(x) for x in category_df[category_df_yaxis]],
                 template = "seaborn")
            st.plotly_chart(fig,use_container_width=True, height = 200)

        with cl2:
            st.subheader(str(category_df_y2axis) + ' Pie Chart')
            fig = px.pie(filtered_df, values = str(category_df_yaxis), names = str(category_df_y2axis), hole = 0.5)
            fig.update_traces(text = filtered_df[category_df_y2axis], textposition = "outside")
            st.plotly_chart(fig,use_container_width=True)

        st.markdown("Column #1 Counts Bar Chart")
        st.bar_chart(df[select_col_1].value_counts())

        st.markdown("Column #2 Line Chart")
        st.line_chart(df[select_col_2])

if __name__ == '__main__':
    main()

