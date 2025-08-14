# Capstone Project Walkthrough 
This repository contains an end-to-end definition of my Capstone Project which is a **NBA Stats ETL (Extract, Transform and Load) Pipeline** and Analysis using **Streamlit**.

## Repository Structure and Commits
TBD

## Project Requirements
The user requires a robust ETL pipeline to integrate NBA games and players information from a CSV file on [Kaggle](https://www.kaggle.com/datasets/patrickhallila1994/nba-data-from-basketball-reference?select=salaries.csv). The pipeline must clean  and standardise the data, remove any invalid or missing entries and retain data only between **2016** and **2021**. Also, the pipeline should enrich the dataset by calculating how points were scored by each player during a game per year. This is so the user can analyse how a player's statistics changed per game and per season. The final cleaned and enriched dataset must be stored in the **Pagila SQL Database** for analysis. The user also requires a Streamlit application which contains visualisations which describe key insights e.g. *How a player's salary increases per season, Does the height of a player and their position affect their salary? Who scored the most three-pointer shots in a season?* etc. 

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
- [ ] The box score data is successfully extracted from the CSV file on Kaggle.
- [ ] The data extraction executes in less than two (2) seconds.
- [ ] Data extraction occurs without any errors and data integrity is preserved.
- [ ] Connection issues to Kaggle are logged and handled gracefully.
- [ ] CSV and file errors are logged and handled gracefully.
- [ ] Data extraction errors are logged and handled gracefully.
- [ ] Successful data extraction is logged.
- [ ] Box score data is stored in a **Pandas** DataFrame for further analysis.
- [ ] Tests are written to verify that the box score data extraction process is successful.
### User-Story-2 
```
As a Data Analyst/Scientist,
I want to be able to extract the games data from the games.csv file 
on Kaggle, so that I can transform it for analysis.
```
#### User-Story-2 Acceptance Criteria
- [ ] The games data is successfully extracted from the CSV file on Kaggle.
- [ ] The data extraction executes in less than two (2) seconds.
- [ ] Data extraction occurs without any errors and data integrity is preserved.
- [ ] Connection issues to Kaggle are logged and handled gracefully.
- [ ] CSV and file errors are logged and handled gracefully.
- [ ] Data extraction errors are logged and handled gracefully.
- [ ] Successful data extraction is logged.
- [ ] Games data is stored in a **Pandas** DataFrame for further analysis.
- [ ] Tests are written to verify that the games data extraction process is successful.
### User-Story-3
```
As a Data Analyst/Scientist,
I want to be able to extract the player information data from the player_info.csv file 
on Kaggle, so that I can transform it for analysis.
```
#### User-Story-3 Acceptance Criteria
- [ ] The player information data is successfully extracted from the CSV file on Kaggle.
- [ ] The data extraction executes in less than two (2) seconds.
- [ ] Data extraction occurs without any errors and data integrity is preserved.
- [ ] Connection issues to Kaggle are logged and handled gracefully.
- [ ] CSV and file errors are logged and handled gracefully.
- [ ] Data extraction errors are logged and handled gracefully.
- [ ] Successful data extraction is logged.
- [ ] Player information data is stored in a **Pandas** DataFrame for further analysis.
- [ ] Tests are written to verify that the player information data extraction process is successful.
### User-Story-4
```
As a Data Analyst/Scientist,
I want to be able to extract the salaries data from the salaries.csv file 
on Kaggle, so that I can transform it for analysis.
```
#### User-Story-4 Acceptance Criteria
- [ ] The salaries data is successfully extracted from the CSV file on Kaggle.
- [ ] The data extraction executes in less than two (2) seconds.
- [ ] Data extraction occurs without any errors and data integrity is preserved.
- [ ] Connection issues to Kaggle are logged and handled gracefully.
- [ ] CSV and file errors are logged and handled gracefully.
- [ ] Data extraction errors are logged and handled gracefully.
- [ ] Successful data extraction is logged.
- [ ] Salaries data is stored in a **Pandas** DataFrame for further analysis.
- [ ] Tests are written to verify that the salaries data extraction process is successful.

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
I want to be able to load the combined box score and games dataset into the Pagila SQl database,
so that it can be queried for visualisations and insights.
```
#### User-Story-9 Acceptance Criteria
- [ ] The combined dataset is successfully loaded into the Pagila SQL database.
- [ ] Connection issues to the Pagila SQL Database are logged and handled gracefully.
- [ ] Successful data loading is logged.
- [ ] Data loading errors are logged and handled gracefully.
- [ ] Tests are written to verify that the data loading process is successful.

### User-Story-10
```
I want to be able to load the combined player information and salaries dataset into the Pagila SQl database,
so that it can be queried for visualisations and insights.
```
#### User-Story-10 Acceptance Criteria
- [ ] The combined dataset is successfully loaded into the Pagila SQL database.
- [ ] Connection issues to the Pagila SQL Database are logged and handled gracefully.
- [ ] Successful data loading is logged.
- [ ] Data loading errors are logged and handled gracefully.
- [ ] Tests are written to verify that the data loading process is successful.

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



