#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import plotly
import plotly.express as px
import pycountry

def get_alph_3(location):
    try:
        return pycountry.countries.get(name=location).alpha_3
    except:
        return None
    
df = pd.read_csv("csv/Corona_13-April-2020_T1240.csv")

# from list(pycountry.countries)
df['Country,Other'][0] = 'United States'
df['Country,Other'][5] = 'United Kingdom'
df['Country,Other'][6] = 'Iran, Islamic Republic of'
df['Country,Other'][13] = 'Russian Federation'
df['Country,Other'][18] = 'Korea, Republic of'
df['Country,Other'][37] = 'United Arab Emirates'
df['Country,Other'][56] = 'Moldova, Republic of'
df['Country,Other'][87] = 'Côte d\'Ivoire'
df['Country,Other'][96] = 'Taiwan, Province of China'
df['Country,Other'][101] = 'Bolivia, Plurinational State of'
df['Country,Other'][105] = 'Palestine, State of'
df['Country,Other'][108] = 'Viet Nam'
df['Country,Other'][110] = 'Congo, The Democratic Republic of the'
df['Country,Other'][116] = 'Faroe Islands'
df['Country,Other'][117] = 'Venezuela, Bolivarian Republic of'
df['Country,Other'][123] = 'Brunei Darussalam'
df['Country,Other'][147] = 'Tanzania, United Republic of'
df['Country,Other'][156] = 'Saint Martin (French part)'
df['Country,Other'][158] = 'Syrian Arab Republic'
df['Country,Other'][183] = 'Saint Vincent and the Grenadines'
df['Country,Other'][184] = 'Central African Republic'
df['Country,Other'][194] = 'Turks and Caicos Islands'
df['Country,Other'][195] = 'Holy See (Vatican City State)'
df['Country,Other'][197] = 'Saint Barthélemy'
df['Country,Other'][201] = 'Falkland Islands (Malvinas)'
df['Country,Other'][206] = 'Virgin Islands, British'
df['Country,Other'][209] = 'Saint Pierre and Miquelon'

# Anadimos el codigo alph al data frame
df['Code'] = df['Country,Other'].apply(lambda x: get_alph_3(x))

# columnas nuevo orden
col_new = [df.columns[-1]]+[df.columns[0]]+[df.columns[-2]]+list(df.columns[1:-2])

df_def=df[col_new]

# Confirmed
fig_c = px.choropleth(df_def, locations='Country,Other', locationmode='country names', 
                      color="TotalCases", hover_name="Country,Other", hover_data=['TotalCases'],
                     color_continuous_scale=px.colors.sequential.Plasma)
fig_c.update_layout(
    title_text = 'Casos Totales Coronavirus')
fig_c.show()
# Deaths

fig_d = px.choropleth(df_def, locations='Country,Other', locationmode='country names',
                       color="TotalDeaths", hover_name="Country,Other", hover_data=['TotalDeaths'],
                     color_continuous_scale=px.colors.sequential.Plasma)

fig_d.update_layout(
    title_text = 'Muertes Totales Coronavirus')
fig_d.show()


# In[ ]:




