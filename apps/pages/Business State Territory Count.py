import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

st.set_page_config(layout='wide')

st.subheader("Business State Territory Count Visualization")

alt.themes.enable("dark")

df = pd.read_csv("MU_REPORT.csv", encoding = 'latin1')

df_states = df["Business_State_Territory"]
counts = df_states.value_counts()

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

unique_values = counts.index
unique_values = pd.DataFrame(unique_values)
unique_values["State_abb"] = [states_abbreviation[x] for x in unique_values["Business_State_Territory"]]

choropleth = px.choropleth(locations=unique_values["State_abb"], 
                            locationmode="USA-states", 
                            color=counts, 
                            scope="usa",
                            labels={'locations':'State','color':'Counts'},
                            color_continuous_scale=px.colors.sequential.YlOrRd
                            )

choropleth.update_layout(
    template = 'plotly_dark',
    )
choropleth

st.markdown("Business State Territory Counts")
state_value_counts = df["Business_State_Territory"].value_counts()
fig = px.bar(state_value_counts,
            color = counts,
            color_continuous_scale=px.colors.sequential.YlOrRd,
            labels={'Business_State_Territory':'State', 'color':''}
            )
fig