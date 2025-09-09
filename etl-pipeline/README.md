![NBA Logo](/etl-pipeline/images/nba_logo.avif)
# HoopMetrics ETL Pipeline

This ETL pipeline successfully extracts, cleans, transforms, enriches and loads the NBA dataset into the Pagila SQL database.

---
## Prerequisites:
Kaggle API Key (for Linux/Mac users): 
- Create or Sign in to [Kaggle](https://www.kaggle.com).
- Go to Account settings and create an API token. This would download a `kaggle.json` file.
- Store this file in:
  - `~/.kaggle/kaggle.json`
  
For Windows users:
- Go to [Kaggle NBA Dataset](https://www.kaggle.com/datasets/patrickhallila1994/nba-data-from-basketball-reference/data?select=boxscore.csv).
- Download the CSVs.
- Create a new directory `data/raw` in `Capstone-Project/etl_pipeline` and save the CSV files here.

**N.B**: One of the functions would fail for Windows users which checks for the Kaggle API key but the pipeline would run fine.

**Local PostgreSQL Instance:**
- Assuming postgreSQL is already set up on your device, connect to your database instance and create a new database using the following:
```bash
# Using psql
psql -U your_db_user

# Create the database
CREATE DATABASE your_db_name;
```
---

## How to Run It:
1. **Clone this repo**:
```bash
git clone https://github.com/AdedoyinAA/Capstone-Project.git
cd Capstone-Project/etl-pipeline
```
2. **Setup virtual environment**:
```bash
python -m venv .venv
# or with python3
python3 -m venv .venv
```
- For Windows:
```bash
source .venv\Scripts\activate
```
- For MacOS/Linux:
```bash
source .venv/bin/activate
```
3. **Install the dependencies**:
```bash
pip install -r requirements.txt
```
4. **Run the project in editable mode**:
```bash
pip install -e .
```
5. **Add `.env.test` file and add these variables (fill with your own database details)**:
```env
TARGET_DB_NAME=<your_db_name>
TARGET_DB_USER=<your_db_user>
TARGET_DB_PASSWORD=<your_db_user_password>
TARGET_DB_HOST=<your_db_host>
TARGET_DB_PORT=<your_db_port>
```
6. **Run the ETL pipeline**:
```bash
run_etl test
# Or run this instead
python -m scripts.run_etl test
```

N.B: After downloading/extracting the CSVs, you only need to keep the `boxscore.csv`, `games.csv`, `player_info.csv` and `salaries.csv` files. The rest can be deleted from the `data/raw` directory.

On Mac/Linux, everytime the pipeline is executed, the entire dataset would be downloaded from Kaggle. To prevent this, you can comment out the `extract_csvs()` function in the `src/extract/extract_boxscores.py` file.


