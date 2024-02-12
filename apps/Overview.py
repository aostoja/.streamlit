import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import altair as alt
import plost

st.sidebar.header('Dashboard')

st.sidebar.subheader('Raw Data Chart Provider Type')
map_select = st.sidebar.selectbox('Select Provider Type', ('EP','Hospital'))

st.sidebar.subheader('Business State Territory Counts Chart Height')
plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)

st.subheader("Business State Territory Count Visualization")

alt.themes.enable("dark")

df = pd.read_csv("MU_REPORT.csv", encoding = 'latin1')

df_filt = df[df['Provider_Type']==map_select]

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

hosp_gen = len(df[df['Hospital_Type']=='General'])
hosp_crit = len(df[df['Hospital_Type']=='Critical Access'])
crit_per = (hosp_crit/(hosp_crit+hosp_gen))*100

prod_comp = len(df[df['Product_Classification']=='Complete EHR'])
prod_mod = len(df[df['Product_Classification']=='Modular EHR'])
prod_per = (prod_comp/(prod_comp+prod_mod))*100

prod_amb = len(df[df['Product_Setting']=='Ambulatory'])
prod_inp = len(df[df['Product_Setting']=='Inpatient'])
prod_s_per = (prod_amb/(prod_amb+prod_inp))*100

col1, col2, col3 = st.columns(3)
col1.metric("Critical Access Hospital Type", str(crit_per)[:5] + "%")
col2.metric("Complete EHR Product Classification", str(prod_per)[:5] + "%")
col3.metric("Ambulatory Product Setting", str(prod_s_per)[:5] + "%")

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
        template = 'plotly_dark'
        )
choropleth

st.markdown("Business State Territory Counts")
state_value_counts = df["Business_State_Territory"].value_counts()
fig = px.bar(state_value_counts,
            color = counts,
            color_continuous_scale=px.colors.sequential.YlOrRd,
            labels={'Business_State_Territory':'State', 'color':''},
            height = plot_height
            )
fig

#subheader
st.subheader("EHR Products Used for Meaningful Use Attestation")

st.markdown("Raw Data from (https://catalog.data.gov/dataset/ehr-products-used-for-meaningful-use-attestation)")

df_filt = df[df['Provider_Type']==map_select]

st.write(df_filt)

st.markdown("Specialty Counts")
st.bar_chart(df["Specialty"].value_counts())

st.markdown("Business State Territory Counts")
st.bar_chart(df["Business_State_Territory"].value_counts())

st.markdown("Program Type Counts")
st.bar_chart(df["Program_Type"].value_counts())

Program_Type_unique = df["Program_Type"].unique()
Program_Type_counts = df["Program_Type"].value_counts()

Program_Type_unique_list = [Program_Type_unique[0], Program_Type_unique[1]]
Program_Type_counts_list = [Program_Type_counts[1], Program_Type_counts[0]]

st.markdown("Program Type Counts Pie Chart")
fig1, ax1 = plt.subplots()
patches, texts, pcts = ax1.pie(Program_Type_counts_list, labels=Program_Type_unique_list, autopct='%1.1f%%',
        shadow=True, startangle=90)
for i, patch in enumerate(patches):
    texts[i].set_color(patch.get_facecolor())
plt.setp(pcts, color='white')
plt.setp(texts, fontweight=600, fontsize=10)
ax1.axis('equal')
fig1.set_facecolor('#111111')

st.pyplot(fig1)

st.markdown("Product Classification Counts")
st.bar_chart(df["Product_Classification"].value_counts())

#df_states

#df["Provider_Type"]

#df_filt = df[df['Provider_Type']==map_select]
#df_filt