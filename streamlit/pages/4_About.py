import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="About",
    layout="wide",
    initial_sidebar_state="auto"
)

# Get the absolute path to the image relative to this file
base_dir = Path(__file__).parent.parent
testing_results_path = base_dir / "images" / "testing_results.png"
project_plan_path = base_dir / "images" / "project_plan.png"

st.markdown("""
# <span style="color:#60b4ff">About HoopMetrics</span> 🏀

Welcome to the <span style="color:#60b4ff">**HoopMetrics**!</span>
- This application
showcases the journey of the raw
[NBA Stats](https://www.kaggle.com/datasets/patrickhallila1994/nba-data\
-from-basketball-reference?select=salaries.csv) dataset to meaningful insights.
- The dataset contained all NBA statistics between 1996 and 2021, but for this
project, a smaller subset was used (2016 to 2021).
- The goal of this project was to provide some insight about the teams and
players based on their calendar year performance.

---

## <span style="color:#60b4ff">Project Plan</span>
""", unsafe_allow_html=True)
st.image(project_plan_path)
st.markdown("""
---

## <span style="color:#60b4ff">Data Journey: ETL Pipeline</span>

The dataset underwent a full **ETL (Extract, Transform, Load) pipeline**:

- **Extraction:** Raw player and team statistics were downloaded and extracted
    from Kaggle.
- **Transformation:** Data cleaning included:
  - Removing special characters and trimming whitespaces from all entries.
  - Appropriate data type conversion e.g: `object` to `datetime`.
  - Handling missing values and ensuring consistent data types.
  - Renaming columns for better understanding.
  - Parsing multi-position players and selecting primary positions for
    analysis.
  - Aggregating statistics to calculate points per game per calendar year, etc.
  - Aggregating player statistics to calculate summary metrics such as median,
  P95, and P99 salaries.
- **Loading:** Cleaned and enriched data was loaded into a PostgreSQL database
    (Pagila) for persistence and efficient querying.
- **Testing:** A total of **107** unit tests were written to assess the
    functionality of the ETL pipeline and a code coverage of **94%**
    was achieved.

### <span style="color:#60b4ff">Testing Results</span>
""", unsafe_allow_html=True)
st.image(testing_results_path)


st.markdown("""
---

## <span style="color:#60b4ff">Key Insights & Takeaways</span>

- Salary distributions vary widely across positions, with all positions
    showing significant outliers.
- Percentile analysis (P95, P99) reveals the impact of top-performing players
    on average salaries.
- Multi-position players were handled thoughtfully to maintain clarity in
    analysis.

---

""", unsafe_allow_html=True)
