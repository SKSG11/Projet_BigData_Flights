import streamlit as st
import pandas as pd
import plotly.express as px
from cassandra.cluster import Cluster

st.set_page_config(page_title="Dashboard Retards de Vols", layout="wide")

st.title("🛫 Dashboard d'Analyse des Retards de Vols (Spark x Cassandra)")
st.caption("Calcul des taux de retards lourds (> 60 minutes) et des durées moyennes par entité.")

@st.cache_resource
def get_cassandra_session():
    cluster = Cluster(['127.0.0.1'])
    return cluster.connect('flight_analytics')

session = get_cassandra_session()
tab1, tab2, tab3 = st.tabs(["Compagnies Aériennes", "Jours de la Semaine", "Aéroports"])

# Tab 1 : Compagnies
with tab1:
    st.header("Analyse par compagnie aérienne")
    rows = session.execute("SELECT airline, delay_rate, avg_delay_minutes, total_flights FROM delays_by_airline;")
    df_airline = pd.DataFrame(rows)
    if not df_airline.empty:
        df_airline['delay_pct'] = df_airline['delay_rate'] * 100
        
        col1, col2 = st.columns(2)
        with col1:
            fig_rate = px.bar(
                df_airline.sort_values('delay_pct', ascending=False), 
                x='airline', 
                y='delay_pct',
                title="Taux de retards lourds (> 1h) par compagnie (%)",
                labels={'airline': 'Compagnie', 'delay_pct': 'Taux de retard (%)'},
                color='delay_pct',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig_rate, use_container_width=True)
        
        with col2:
            fig_avg = px.bar(
                df_airline.sort_values('avg_delay_minutes', ascending=False), 
                x='airline', 
                y='avg_delay_minutes',
                title="Retard moyen à l'arrivée (minutes)",
                labels={'airline': 'Compagnie', 'avg_delay_minutes': 'Retard moyen (min)'},
                color='avg_delay_minutes',
                color_continuous_scale='Oranges'
            )
            st.plotly_chart(fig_avg, use_container_width=True)
            
        st.dataframe(df_airline)

# Tab 2 : Jours de la Semaine
with tab2:
    st.header("Analyse selon le jour de la semaine")
    rows = session.execute("SELECT day_of_week, delay_rate, avg_delay_minutes, total_flights FROM delays_by_weekday;")
    df_weekday = pd.DataFrame(rows)
    if not df_weekday.empty:
        days_map = {1: 'Lundi', 2: 'Mardi', 3: 'Mercredi', 4: 'Jeudi', 5: 'Vendredi', 6: 'Samedi', 7: 'Dimanche'}
        df_weekday['day_name'] = df_weekday['day_of_week'].map(days_map)
        df_weekday['delay_pct'] = df_weekday['delay_rate'] * 100
        df_weekday = df_weekday.sort_values('day_of_week')
        
        fig_week = px.line(
            df_weekday, 
            x='day_name', 
            y='delay_pct', 
            markers=True,
            title="Évolution du taux de retards lourds au cours de la semaine (%)",
            labels={'day_name': 'Jour', 'delay_pct': 'Taux de retard (%)'}
        )
        st.plotly_chart(fig_week, use_container_width=True)
        st.dataframe(df_weekday)

# Tab 3 : Aéroports
with tab3:
    st.header("Analyse par aéroport d'origine")
    rows = session.execute("SELECT airport_code, flight_date, delay_rate, avg_delay_minutes, total_flights FROM delays_by_airport LIMIT 100;")
    df_airport = pd.DataFrame(rows)
    if not df_airport.empty:
        df_airport['delay_pct'] = df_airport['delay_rate'] * 100
        st.dataframe(df_airport)