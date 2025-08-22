![NBA Logo](/etl-pipeline/images/nba_logo.avif)
# Capstone Project Overview
This repository contains an end-to-end definition of my Capstone Project which is a **NBA Stats ETL (Extract, Transform and Load) Pipeline** and Analysis using **Streamlit**.

## Repository Structure
<pre>
├── etl-pipeline
│   ├── config
│   ├── data
│   │   ├── processed               # Cleaned CSVs
│   │   └── raw                     # Unprocessed CSVs downloaded from Kaggle
│   ├── images                      # Images
│   ├── notebooks                   # Used for EDA
│   ├── README.md                   # Documentation for the ETL pipeline
│   ├── requirements-setup.txt      # Dependencies to set up the Python project
│   ├── requirements.txt            # Dependencies to set up virtual environment for ETL pipeline
│   ├── scripts                     # Contains the script that runs the ETL pipeline
│   ├── src                         
│   │   ├── extract                 # Contains scripts for downloading and extracting the CSV data
│   │   ├── load                    # Contains scripts for loading the enriched data into Pagila
│   │   ├── logs                    # Handles logging
│   │   ├── transform               # Contains scripts for transforming the extracted dataset
│   │   └── utils                   # Reusable helper functions
│   └── tests
│       ├── test_data               # Cleaned data for testing
│       └── unit_tests              # Unit Tests
├── README.md                       # Documentation for entire project
└── streamlit
    ├── Home.py                     # Main page for the Streamlit application
    ├── images                      # Images
    ├── pages                       # Additional pages for the Streamlit application
    ├── README.md                   # Documentation for the Streamlit application
    ├── requirements.txt            # Dependencies to set up virtual environment for the Streamlit application
    ├── sql                         # SQL scripts for querying Pagila 
    └── utils                       # Reusable helper functions
</pre>
## Project Requirements
A robust ETL pipeline which integrates NBA games and players information from CSV files on [Kaggle](https://www.kaggle.com/datasets/patrickhallila1994/nba-data-from-basketball-reference?select=salaries.csv). The pipeline cleans and standardises the data, removes any invalid or missing entries and retains data only between **2016** and **2021**. Also, the pipeline enriches the dataset by calculating the average points scored by each player per year and a variety of other stats(rebounds per game, assists per game, etc). This is so the user can analyse how a player or team's statistics changed per season. The final cleaned and enriched dataset is stored in the **Pagila SQL Database** for analysis. A Streamlit application is also designed which contains key insights and visualisations e.g. *Which team won the most of their games in a year? Does the height, weight and position of a player influence their salary in any way? Who scored the most three-pointers?* etc. 

## Project Dataset
> [NBA Data from 1996 to 2021](https://www.kaggle.com/datasets/patrickhallila1994/nba-data-from-basketball-reference/data?select=boxscore.csv)

## Project Requirements as an Epic
```
As the User,
I want a robust and complete ETL pipeline that integrates, cleans, standardises, and enriches 
NBA Statistics data from Kaggle, retaining only data between 2016 and 2021 so that key statistics 
for players and teams and the enriched dataset are loaded into the Pagila SQL database so I can access a 
Streamlit application which has key insights and visualisations.
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
I want to be able to extract the box scores data from the boxscore.csv file 
on Kaggle, so that I can transform it for analysis.
```
#### User-Story-1 Acceptance Criteria
- [X] The box score data is successfully extracted from the CSV file on Kaggle.
- [X] Data extraction occurs without any errors and data integrity is preserved.
- [X] Connection issues to Kaggle are logged and handled gracefully.
- [X] CSV and file errors are logged and handled gracefully.
- [X] Data extraction errors are logged and handled gracefully.
- [X] Successful data extraction is logged.
- [X] Box scores data is stored in a **Pandas** DataFrame for further analysis.
- [X] Tests are written to verify that the box score data extraction process is successful.
### User-Story-2 
```
As a Data Analyst/Scientist,
I want to be able to extract the games data from the games.csv file 
on Kaggle, so that I can transform it for analysis.
```
#### User-Story-2 Acceptance Criteria
- [X] The games data is successfully extracted from the CSV file on Kaggle.
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
I want to be able to access cleaned and standardised box scores data, 
so that it can be merged with the games data for further analysis.
```
### User-Story-6
```
I want to be able to access cleaned and standardised games data,
so that it can be merged with the box scores data for further analysis.
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
I want to be able to load the combined box scores and games datasets into the Pagila SQL database,
so that it can be queried for visualisations and insights.
```
#### User-Story-9 Acceptance Criteria
- [X] The combined datasets are successfully loaded into the Pagila SQL database.
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
I want to be able to view key insights about the cleaned and enriched dataset on Streamlit by querying the Pagila SQL database.
```
### User-Story-11
```
I want to be able to access a Streamlit application which shows visualisations and key insights 
about the cleaned and enriched NBA dataset.
```
---

## Definition of Done
- [X] All subtasks are completed.
- [X] Code coverage is at least 80%.
- [X] All tests are passing.
- [X] Code is linted and follows style guidelines (e.g. PEP8 for Python code).
- [X] All performance metrics are met.
- [X] Documentation is updated.
- [X] Code is merged into the main branch.
  
---

## Project Kanban Board
GitHub Projects was used to create Kanban boards for each user story.
### Activity 1 - Project Environment Setup
> This was done by forking the `initial-project-setup` branch in the `new-etl-project-walkthrough` repo.
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

---

### Activity 5 - Streamlit Application
#### Develop Streamlit Application - Epic-4-Story-11
[Story-11 Board](https://github.com/users/AdedoyinAA/projects/20)

---

**N.B**: To see information about both the pipeline and the streamlit application specifically, reference their respective `README.md` files in the `etl-pipeline` and `streamlit` directories.

---

## Scalability, Security & Deployment Considerations
### Query Execution & Performance Optimisation
As the dataset grows, optimising query execution becomes increasingly important.
- **Database indexing**: Creating indexes on frequently queried columns (e.g., `player_name`, `year`) to speed up lookups.
- **Query optimisation**: Using `EXPLAIN` in PostgreSQL to identify bottlenecks, rewriting subqueries as joins, and minimising unnecessary aggregations.
- **ETL performance**: Parallelising data ingestion using multiprocessing and leveraging bulk insert operations.

### Error Handling & Logging
Throughout the pipeline, I added structured error handling and logging to ensure visibility into failures:
- **Error handling**:
    - Raised `FileNotFoundError` when SQL files were missing.
    - Raised `QueryExecutionError` for database execution issues.
    - Used Streamlit `st.error()` for user-facing errors.
- **Logging**:
    - Implemented `logger.info()` for tracking ETL steps (e.g., table creation/replacement).
    - Logged warnings for suspicious data (e.g., missing values, invalid formats).
    - Logged errors for debugging.
This logging can be integrated with monitoring tools (e.g., CloudWatch, ELK stack) in production for better observability.

### Security & Privacy Considerations
- **Application security**:
    - Streamlit app can be protected with authentication (e.g., AWS Cognito, OAuth).
  
### Deployment & Cloud Automation (AWS)
This project could be scaled and automated in AWS:
- **Data storage**:
    - Store raw data in **S3**.
    - Use **AWS Glue** for ETL orchestration and schema discovery.
- **Database**:
    - Load processed data into **Amazon RDS (PostgreSQL)** or **Redshift** for analytics at scale.
- **Compute**:
    - Deploy the ETL pipeline on **AWS Lambda** (event-driven) or **ECS/EKS** (containerised).
- **Visualisation**:
    - Deploy the Streamlit app on **EC2** or as a container in **ECS/EKS** with a load balancer.
    - Alternatively, migrate dashboards to Amazon QuickSight for enterprise-ready BI.
- **Automation**:
    - Use **Step Functions** or **Airflow** on **MWAA** to orchestrate the pipeline end-to-end.
    - Schedule ETL runs using **EventBridge** (**CloudWatch Events**).
