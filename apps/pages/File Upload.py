import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_icon=":bar_chart:",layout="wide")
st.title('Streamlit Dashboard - Upload Dataset')
st.sidebar.header('Parameters')

states_abbreviation = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District Of Columbia": "DC",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands": "VI",
    "Federated States Of Micronesia": "UM",
    "Palau": "UM",
    "Marshall Islands": "UM"
}

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
        
        mult_val_columns = list(filter(lambda x: df[x].nunique() < 50, df.columns))

        with col1:
            category_df_xaxis = st.selectbox('Select Category', mult_val_columns)
        with col2:
            category_df_yaxis = st.selectbox('Select Quantity Column', df.columns)
        with col3:
            category_df_y2axis = st.selectbox('Select Pie Chart Category', mult_val_columns)
        category_df = filtered_df.groupby(by = [category_df_xaxis], as_index = False)[category_df_yaxis].sum()

        col1.metric(category_df_yaxis +' Mean Value', np.round(filtered_df[category_df_yaxis].mean()))
        col2.metric(category_df_yaxis +' Maximum Value', filtered_df[category_df_yaxis].max())
        col3.metric(category_df_yaxis +' Minimum Value', filtered_df[category_df_yaxis].min())

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

        state_col = []
        kkf = df.columns.tolist()
        for state in kkf:
            if 'state' in state:
                state_col.append(state)
            elif 'State' in state:
                state_col.append(state)
            elif 'STATE' in state:
                state_col.append(state)
            else:
                pass
        if len(state_col) == 1:
            df_states = filtered_df[state_col[0]]
            counts = df_states.value_counts()
            unique_values = counts.index
            unique_values = pd.DataFrame(unique_values)
            unique_values["State_abb"] = [states_abbreviation[x] for x in unique_values[state_col[0]]]
            choropleth = px.choropleth(locations=unique_values['State_abb'], 
                            locationmode="USA-states", 
                            color=counts, 
                            scope="usa",
                            labels={'locations':'State','color':'Counts'},
                            color_continuous_scale=px.colors.sequential.YlOrRd
                            )
            choropleth.update_layout(
                template = 'plotly_dark',
                margin = dict(l=10, r=10, t=0, b=0),
                width = 800,
                height = 600
                )
            st.write("<h1 style='text_align: center;'>Choropleth Map Presenting Counts per State</h1>", unsafe_allow_html=True)
            st.plotly_chart(choropleth, use_container_width = True)
        st.markdown("Column #1 Counts Bar Chart")
        st.bar_chart(df[select_col_1].value_counts())

        st.markdown("Column #2 Line Chart")
        st.line_chart(df[select_col_2])
if __name__ == '__main__':
    main()

