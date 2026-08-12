# Projet Big Data : Analyse des Retards de Vols Aériens

Ce projet met en place une chaîne Big Data de traitement et d'analyse NoSQL des retards de vols à l'aide de **PySpark** et **Apache Cassandra**, orchestrée sous **Docker** et visualisée via **Streamlit**.

## Architecture du Projet

1. **Ingestion & Traitement Distribué** : PySpark 3.5 nettoie le jeu de données (`Flight_delay.csv`) et calcule 3 agrégats clés :
   - Taux de retards lourds (> 60 min) et temps moyen par aéroport d'origine et par date.
   - Taux de retards lourds et temps moyen par compagnie aérienne.
   - Taux de retards lourds et temps moyen par jour de la semaine.
2. **Stockage NoSQL** : Apache Cassandra enregistre les résultats selon une modélisation orientée colonnes ciblée (*Query-First*).
3. **Visualisation** : Un dashboard interactif Streamlit / Plotly lit directement les agrégats dans Cassandra.

## Structure du Dépôt

```text
.
├── docker-compose.yml          # Configuration du conteneur Cassandra
├── schema.cql                  # Définition du Keyspace et des tables Cassandra
├── Flight_delay.csv            # Jeu de données 
├── process_flights.py          # Pipeline PySpark (lecture, transformation, écriture Cassandra)
├── app_viz.py                  # Dashboard Streamlit (Visualisation NoSQL)
├── requirements.txt            # Dépendances Python
├── Rapport_Projet_BigData.docx # Rapport de projet         
└── README.md                   # Documentation du projet
