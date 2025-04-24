# Exploring the Impact of Air Pollution on Public Health and Transport in Irish Cities

This project analyzes the connection between air pollution, hospital admissions, and public transport usage in Dublin, Cork, and Limerick.

## Team Members
- Krishnali Lahane (Lead Developer & Dashboard)
- Indrajit Diwane (Data Extraction & Preprocessing)
- Ridhi Sharma (Visualization & Insights)

## What We Did
- Extracted pollution data from the EPA API
- Parsed CSO JSON for hospital admissions
- Cleaned transport usage CSV data
- Built a full ETL pipeline using Python, MongoDB, and PostgreSQL
- Created a Streamlit dashboard for interactive analysis

## Project Structure
- `notebooks/`: Jupyter development notebook
- `dashboard/`: Streamlit app code
- `report/`: Word report, slides, and flowcharts
- `figures/`: Output charts used in the report
- `sql/`: Optional DB schema setup
  
### 🔗 Data Source Note
Full air pollution data (~117,000+ records) was fetched live via the [EPA Ireland Open API](https://data.epa.ie/air/api/v1/measurements).  
Due to size constraints, only a small sample (`pollution_sample.csv`) is included here. You can regenerate the full dataset using our API code in `Code.ipynb`.

## How to Run
1. Clone the repo
2. Set up a virtual environment
3. Install packages: `pip install -r requirements.txt`
4. Run dashboard: `streamlit run dashboard/dashboard.py`

## Dependencies
- pandas, numpy, matplotlib, altair, streamlit, sqlalchemy, requests

