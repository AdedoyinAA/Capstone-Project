# NBA Stats ETL Pipeline

This ETL pipeline successfully extracts, cleans, transforms, enriches and loads the dataset into the Pagila SQL database.

---

## How to Run It:
1. **Clone this repo**:
```bash
git clone https://github.com/AdedoyinAA/Capstone-Project.git
cd CapStone-Project/etl-pipeline
```
2. **Setup virtual environment**:
```bash
python3 -m venv .venv
```
- For Windows
```bash
source .venv/Scripts/activate
```
- For MacOS/Linux
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
5. **Add `.env` file and add these variables (fill with your own database details)**:
```env
TARGET_DB_NAME=<your_db_name>
TARGET_DB_USER=<your_db_user>
TARGET_DB_PASSWORD=<your_db_user_password>
TARGET_DB_HOST=<your_db_host>
TARGET_DB_PORT=<your_db_port>
```
6. **Run the ETL pipeline**:
```bash
run_etl prod
```

