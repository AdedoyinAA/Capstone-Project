![Alt text](./etl-pipeline/images/NBA.Com-National-Basketball-Association.png.avif)
# Capstone Project Overview
This repository contains an end-to-end definition of my Capstone Project which is a **NBA Stats ETL (Extract, Transform and Load) Pipeline** and Analysis using **Streamlit**.

## Repository Structure
<pre>
├── etl-pipeline
│   ├── config
│   ├── data
│   │   ├── processed               # Cleaned CSVs 
│   │   └── raw                     # Unprocessed CSVs downloaded from Kaggle 
│   ├── notebooks                   # Used for EDA    
│   ├── requirements.txt            # Dependencies to set up virtual environment
│   ├── scripts                     # Contains script that runs ETL pipeline
│   ├── src
│   │   ├── extract                 # Downloads and extracts the CSV data from kaggle
│   │   ├── load                    # Loads the data into the Pagila SQL database
│   │   ├── logs                    # Handles logging for the project
│   │   ├── sql                     # SQL scripts for loading
│   │   ├── transform               # Cleaning and enriching the dataset
│   │   └── utils   
│   └── tests                       # Testing ETL pipeline
├── README.md
└── streamlit
</pre>
## Project Requirements
A robust ETL pipeline which integrates NBA games and players information from CSV files on [Kaggle](https://www.kaggle.com/datasets/patrickhallila1994/nba-data-from-basketball-reference?select=salaries.csv). The pipeline cleans and standardises the data, removes any invalid or missing entries and retains data only between **2014** and **2019**. Also, the pipeline enriches the dataset by calculating how points were scored by each player during a game per year. This is so the user can analyse how a player's statistics changed per game and per season. The final cleaned and enriched dataset is stored in the **Pagila SQL Database** for analysis. A Streamlit application is also designed which contains key insights and visualisations e.g. *How a player's salary increases per season, Does the height of a player and their position affect their salary? Who scored the most three-pointer shots in a season?* etc. 

## Project Dataset
> https://www.kaggle.com/datasets/patrickhallila1994/nba-data-from-basketball-reference/data?select=boxscore.csv

## Project Requirements as an Epic
```
As the User,
I want a robust and complete ETL pipeline that integrates, cleans, standardises, and enriches 
NBA Statistics data from Kaggle, retaining only data between 2016 and 2021 so that key statistics 
for players and teams and the enriched dataset should be loaded into the Pagila SQL database so it 
can be for a Streamlit application with visualisations representing key insights.
```

---

## Epic-1
```
As a Data Analyst/Scientist,
I want to be able to access the NBA Statistics data,
so that it can be transformed for further analysis.
```

---

## Epic-2
```
As a Data Analyst/Scientist, 
I want to be able to access clean, standardised, enriched and aggregated data,
so that I can make any further analysis much easier.
```

---

## Epic-3
```
As a Data Analyst/Scientist,
I want to be able to load the clean and enriched dataset into the Pagila SQL
database, so it can be used for the Streamlit application.
```

---

## Epic-4
```
As a Data Analyst/Scientist,
I want to be able to view key insights about the cleaned and enriched dataset 
on Streamlit by querying the Pagila SQL database.
```

---

## Epic-1: Breakdown
```
As a Data Analyst/Scientist,
I want to be able to access the NBA Statistics data,
so that it can be transformed for further analysis.
```
### User-Story-1 
```
As a Data Analyst/Scientist,
I want to be able to extract the box score data from the boxscore.csv file 
on Kaggle, so that I can transform it for analysis.
```
#### User-Story-1 Acceptance Criteria
- [X] The box score data is successfully extracted from the CSV file on Kaggle.
- [X] The data extraction executes in less than two (2) seconds.
- [X] Data extraction occurs without any errors and data integrity is preserved.
- [X] Connection issues to Kaggle are logged and handled gracefully.
- [X] CSV and file errors are logged and handled gracefully.
- [X] Data extraction errors are logged and handled gracefully.
- [X] Successful data extraction is logged.
- [X] Box score data is stored in a **Pandas** DataFrame for further analysis.
- [X] Tests are written to verify that the box score data extraction process is successful.
### User-Story-2 
```
As a Data Analyst/Scientist,
I want to be able to extract the games data from the games.csv file 
on Kaggle, so that I can transform it for analysis.
```
#### User-Story-2 Acceptance Criteria
- [X] The games data is successfully extracted from the CSV file on Kaggle.
- [X] The data extraction executes in less than two (2) seconds.
- [X] Data extraction occurs without any errors and data integrity is preserved.
- [X]  Connection issues to Kaggle are logged and handled gracefully.
- [X] CSV and file errors are logged and handled gracefully.
- [X] Data extraction errors are logged and handled gracefully.
- [X] Successful data extraction is logged.
- [X] Games data is stored in a **Pandas** DataFrame for further analysis.
- [X] Tests are written to verify that the games data extraction process is successful.
### User-Story-3
```
As a Data Analyst/Scientist,
I want to be able to extract the player information data from the player_info.csv file 
on Kaggle, so that I can transform it for analysis.
```
#### User-Story-3 Acceptance Criteria
- [X] The player information data is successfully extracted from the CSV file on Kaggle.
- [X] The data extraction executes in less than two (2) seconds.
- [X] Data extraction occurs without any errors and data integrity is preserved.
- [X] Connection issues to Kaggle are logged and handled gracefully.
- [X] CSV and file errors are logged and handled gracefully.
- [X] Data extraction errors are logged and handled gracefully.
- [X] Successful data extraction is logged.
- [X] Player information data is stored in a **Pandas** DataFrame for further analysis.
- [X] Tests are written to verify that the player information data extraction process is successful.
### User-Story-4
```
As a Data Analyst/Scientist,
I want to be able to extract the salaries data from the salaries.csv file 
on Kaggle, so that I can transform it for analysis.
```
#### User-Story-4 Acceptance Criteria
- [X] The salaries data is successfully extracted from the CSV file on Kaggle.
- [X] The data extraction executes in less than two (2) seconds.
- [X] Data extraction occurs without any errors and data integrity is preserved.
- [X] Connection issues to Kaggle are logged and handled gracefully.
- [X] CSV and file errors are logged and handled gracefully.
- [X] Data extraction errors are logged and handled gracefully.
- [X] Successful data extraction is logged.
- [X] Salaries data is stored in a **Pandas** DataFrame for further analysis.
- [X] Tests are written to verify that the salaries data extraction process is successful.

---

## Epic-2: Breakdown
```
As a Data Analyst/Scientist, 
I want to be able to access clean, standardised, enriched and aggregated data,
so that I can make any further analysis much easier.
```
### User-Story-5
```
I want to be able to access cleaned and standardised box score data, 
so that it can be merged with the games data and made available as a single dataset.
```
### User-Story-6
```
I want to be able to access cleaned and standardised games data,
so that it can be merged with the box score data and made available as a single dataset.
```
### User-Story-7
```
I want to be able to access cleaned and standardised player information data,
so that it can be merged with the salaries data and made available as a single dataset.
```
### User-Story-8
```
I want to be able to access cleaned and standardised salaries data,
so that it can be merged with the players information data and made available as a single dataset.
```
--- 

## Epic-3: Breakdown
```
As a Data Analyst/Scientist,
I want to be able to load the clean and enriched dataset into the Pagila SQL
database, so it can be used for the Streamlit application.
```
### User-Story-9
```
I want to be able to load the combined box score and games dataset into the Pagila SQL database,
so that it can be queried for visualisations and insights.
```
#### User-Story-9 Acceptance Criteria
- [X] The combined dataset is successfully loaded into the Pagila SQL database.
- [X] Connection issues to the Pagila SQL Database are logged and handled gracefully.
- [X] Successful data loading is logged.
- [X] Data loading errors are logged and handled gracefully.
- [X] Tests are written to verify that the data loading process is successful.

### User-Story-10
```
I want to be able to load the combined player information and salaries dataset into the Pagila SQL database,
so that it can be queried for visualisations and insights.
```
#### User-Story-10 Acceptance Criteria
- [X] The combined dataset is successfully loaded into the Pagila SQL database.
- [X] Connection issues to the Pagila SQL Database are logged and handled gracefully.
- [X] Successful data loading is logged.
- [X] Data loading errors are logged and handled gracefully.
- [X] Tests are written to verify that the data loading process is successful.

---

## Epic-4: Breakdown
```
As a Data Analyst/Scientist,
I want to be able to view key insights about the cleaned and enriched dataset 
on Streamlit by querying the Pagila SQL database.
```
### User-Story-11
```
I want to be able to access a Streamlit application which shows visualisations
and key insights about the cleaned and enriched NBA dataset.
```
---

## Definition of Done
- [ ] All subtasks are completed.
- [ ] Code coverage is at least 80%.
- [ ] All tests are passing.
- [ ] Code is linted and follows style guidelines (e.g. PEP8 for Python code).
- [ ] All performance metrics are met.
- [ ] Documentation is updated.
- [ ] Code is merged into the main branch.
  
---

## Project Kanban Board
GitHub Projects was used to create Kanban boards for each user story.

### Activity 2 - Extracting the Data
#### Extract Box Scores Data - Epic-1-Story-1
[Story-1 Board](https://github.com/users/AdedoyinAA/projects/3)
#### Extract Games Data - Epic-1-Story-2
[Story-2 Board](https://github.com/users/AdedoyinAA/projects/7)
#### Extract Player Information Data - Epic-1-Story-3
[Story-3 Board](https://github.com/users/AdedoyinAA/projects/8)
#### Extract Salaries Data - Epic-1-Story-4
[Story-4 Board](https://github.com/users/AdedoyinAA/projects/9)

---

### Activity 3 - Transforming the Data
#### Transform Box Scores Data - Epic-2-Story-5
[Story-5 Board](https://github.com/users/AdedoyinAA/projects/10)
#### Transform Games Data - Epic-2-Story-6
[Story-6 Board](https://github.com/users/AdedoyinAA/projects/12)
#### Transform Player Information Data - Epic-2-Story-7
[Story-7 Board](https://github.com/users/AdedoyinAA/projects/16)
#### Transform Salaries Data - Epic-2-Story-8
[Story-8 Board](https://github.com/users/AdedoyinAA/projects/13)

---

### Activity 4 - Loading the Data
#### Load Player Stats and Team Stats Data - Epic-3-Story-9
[Story-9 Board](https://github.com/users/AdedoyinAA/projects/18)
#### Load Player Information and Salaries - Epic-3-Story-10
[Story-10 Board](https://github.com/users/AdedoyinAA/projects/19)




