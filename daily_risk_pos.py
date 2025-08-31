#!/usr/bin/env python
# coding: utf-8
### IMPORTS ###
import scipy
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import altair as alt
import math

### PAGE CONFIGURATION ###
st.set_page_config(
     page_title="BUNGE : Daily risk position assessment",
     page_icon="📊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "# Bienvenue ! # \n"
         "Xavier, Aurélie, Charles, Guillaume et Périnne \n"
     }
)

### SIDEBAR ###
with st.sidebar:
   st.image("img/logo.png", use_container_width=True)
   fp = st.sidebar.file_uploader("Téléversez un fichier Excel", type=["xlsx", "xls"])
   st.image("img/excel_arrow.png", use_container_width=True)

try:
    if fp is not None:
        ### DATAS IMPORT ###
        df_d1 = pd.read_excel(fp, sheet_name=1)
        df_d2 = pd.read_excel(fp, sheet_name=0)

        ### FUNCTIONS ###
        def totalbalance(dataframe):
            try:
                dataframe['Position Date'] = dataframe['Position Date'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y'))
                dataframe['Position Date'] = dataframe['Position Date'].apply(lambda x: datetime.strftime(x, '%Y/%m'))
            except:
                pass
            return pd.pivot_table(dataframe, values='MTM Quantity', index='Position Date', aggfunc='sum')

        def totalbalance_material(dataframe):
            try:
                dataframe['Position Date'] = dataframe['Position Date'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y'))
                dataframe['Position Date'] = dataframe['Position Date'].apply(lambda x: datetime.strftime(x, '%Y/%m'))
            except:
                pass
            return pd.pivot_table(dataframe, values='MTM Quantity', index=['Position Date', 'Material'], aggfunc='sum')

        def totalbalance_countries(dataframe):
            try:
                dataframe['Position Date'] = dataframe['Position Date'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y'))
                dataframe['Position Date'] = dataframe['Position Date'].apply(lambda x: datetime.strftime(x, '%Y/%m'))
            except:
                pass
            return pd.pivot_table(dataframe, values='MTM Quantity', index=['Position Date', 'Incoterm Loc Country'], aggfunc='sum')

        def posneg(valeur):
            if valeur < 0:
                return 'negative'
            else:
                return 'positive'

        def color_negative_red(value):
            if value < 0:
                color = 'red'
            elif value > 0:
                color = 'green'
            else:
                color = 'black'
            return 'color: %s' % color

        ### DATA PREP ###
        balance_d2 = totalbalance(df_d2).reset_index()
        balance_d2 = balance_d2.loc[balance_d2['Position Date']>'2022/03']
        balance_d1 = totalbalance(df_d1).reset_index()
        balance_d1 = balance_d1.loc[balance_d1['Position Date']>'2022/03']
        balance_d2_d1 = (totalbalance(df_d1) - totalbalance(df_d2)).reset_index()
        balance_d2_d1 = balance_d2_d1.loc[balance_d2_d1['Position Date']>'2022/03']

        materialbalance_d2 = totalbalance_material(df_d2).reset_index()
        materialbalance_d2 = materialbalance_d2.loc[materialbalance_d2['Position Date']>'2022/03']
        materialbalance_d1 = totalbalance_material(df_d1).reset_index()
        materialbalance_d1 = materialbalance_d1.loc[materialbalance_d1['Position Date']>'2022/03']
        materialbalance_d2_d1 = (totalbalance_material(df_d1) - totalbalance_material(df_d2)).reset_index()
        materialbalance_d2_d1 = materialbalance_d2_d1.loc[materialbalance_d2_d1['Position Date']>'2022/03']

        countrybalance_d2 = totalbalance_countries(df_d2).reset_index()
        countrybalance_d2 = countrybalance_d2.loc[countrybalance_d2['Position Date']>'2022/03']
        countrybalance_d1 = totalbalance_countries(df_d1).reset_index()
        countrybalance_d1 = countrybalance_d1.loc[countrybalance_d1['Position Date']>'2022/03']
        countrybalance_d2_d1 = (totalbalance_countries(df_d1) - totalbalance_countries(df_d2)).reset_index()
        countrybalance_d2_d1 = countrybalance_d2_d1.loc[countrybalance_d2_d1['Position Date']>'2022/03']

        ### TITLE ###
        original_title = '<p style="font-family: monaco; color:#034C8C; font-size: 40px;">DAY-TO-DAY RISK POSITION ASSESSMENT</p>'
        st.markdown(original_title, unsafe_allow_html=True)

        ### 1ST PART : TOTAL BALANCE BETWEEN TWO DAYS ###
        col1, col2, col3 = st.columns((1,5,1))

        with col2:
            fig1 = px.bar(balance_d2, x='Position Date', y='MTM Quantity', color_discrete_sequence=['#034C8C'])
            fig2 = px.bar(balance_d1, x='Position Date', y='MTM Quantity', color_discrete_sequence=['#D97C2B'])
            fig4 = go.Figure(data=fig1.data + fig2.data)
            fig4.update_layout(
                title="D-2 (blue) and D-1 (orange) risk position",
                title_x=0.5,
                xaxis_title="Months",
                yaxis_title="Quantity sum (t)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
            )
            fig4.update_traces(showlegend=True)
            st.plotly_chart(fig4, use_container_width=True)

        col1, col2, col3 = st.columns((1,5,1))

        with col1:
            st.image("img/left_arrow.png", use_container_width=True)

        with col2:
            fig = px.bar(balance_d2_d1, x='Position Date', y='MTM Quantity', color_discrete_sequence=['#034C8C'])
            fig.update_layout(
                title="Delta",
                title_x=0.5,
                xaxis_title="Months",
                yaxis_title="Quantity sum (t)",
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

        ### SECOND PART : HOW TO EXPLAIN DELTA ###
        sub_title = '<p style="font-family: monaco; color:#034C8C; font-size: 35px;">How to explain the variation ?</p>'
        st.markdown(sub_title, unsafe_allow_html=True)

        material_title = '<p style="font-family: monaco; color:#034C8C; font-size: 25px;">Materials :</p>'
        st.markdown(material_title, unsafe_allow_html=True)

        materialbalance_d2_d1['MTM Absolute Quantity'] = materialbalance_d2_d1['MTM Quantity'].apply(lambda x: abs(x))
        balance_d2_d1['MTM Absolute Quantity'] = balance_d2_d1['MTM Quantity'].apply(lambda x: abs(x))

        selectionMois = st.selectbox(label="Choose a month :", options=materialbalance_d2_d1['Position Date'].value_counts().index.sort_values())
        delta_month = materialbalance_d2_d1[['Position Date','Material','MTM Quantity', 'MTM Absolute Quantity']].loc[materialbalance_d2_d1['Position Date']==selectionMois].sort_values(by='Material')
        delta_month = delta_month.loc[delta_month['MTM Quantity']!=0.0]
        delta_month = delta_month.sort_values(by='MTM Absolute Quantity', ascending=False)
        delta_month = delta_month[['Position Date','Material','MTM Quantity']]
        st.dataframe(delta_month.style.applymap(color_negative_red, subset=['MTM Quantity']))

        countries_title = '<p style="font-family: monaco; color:#034C8C; font-size: 25px;">Countries :</p>'
        st.markdown(countries_title, unsafe_allow_html=True)

        countrybalance_d2_d1 = countrybalance_d2_d1.loc[countrybalance_d2_d1['MTM Quantity']!=0]
        countrybalance_d2_d1.dropna(inplace=True)
        countrybalance_d2_d1['MTM Quantity absolute'] = countrybalance_d2_d1['MTM Quantity'].apply(lambda x: abs(math.log(abs(x))))
        countrybalance_d2_d1['Incoterm Loc Country'] = countrybalance_d2_d1['Incoterm Loc Country'].apply(lambda x: x.lower())
        countrybalance_d2_d1['negative/positive'] = countrybalance_d2_d1['MTM Quantity'].apply(lambda x: posneg(x))

        figmap = px.scatter_geo(
            countrybalance_d2_d1,
            locations="Incoterm Loc Country",
            locationmode='country names',
            size='MTM Quantity absolute',
            hover_data=['MTM Quantity'],
            animation_frame="Position Date",
            color='negative/positive',
            projection="natural earth"
        )
        st.plotly_chart(figmap, use_container_width=True)

    else:
        st.warning("Veuillez téléverser un fichier Excel pour continuer.")

except Exception as e:
    st.error(f"Une erreur est survenue : {e}")
