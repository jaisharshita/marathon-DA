# Ultra Marathon Race Data Analytics Dashboard

### Project Overview
This data analytics project performs a full Exploratory Data Analysis (EDA) on a comprehensive global ultra marathon dataset spanning two centuries. <br> It implements an interactive analytical framework to extract deep insights into runner demographics, race performance, environmental factors, and event competitiveness. <br>The repository contains a complete pipeline moving from raw data ingestion to an interactive web application.<br> (the dataset is taken from kaggle)

### Tech Stack
* **Language:** Python<br>
* **Data Manipulation:** Pandas, NumPy<br>
* **Data Visualization:** Plotly Express, Seaborn, Matplotlib<br>
* **Web Framework:** Streamlit (for the interactive analytics dashboard)<br>
* **Environment:** Jupyter Notebook (for initial EDA and profiling)<br>

### Data Preprocessing and Cleaning Pipeline
The raw dataset contains over 7.4 million rows of data across 13 columns. To perform a focused exploration, the pipeline applies the following granular constraints and transformations:<br>
* **Target Filtering:** Isolates races that took place exclusively in the year 2020, matching 50km or 50mi distances, and localized to the USA.<br>
* **Feature Engineering:** Calculates absolute runner age dynamically using `2020 - Athlete year of birth`.<br>
* **String Parsing:** Standardizes `Athlete performance` timestamps by stripping whitespace and non-numeric suffixes like "h".<br>
* **Name Text Optimization:** Cleans race descriptions by isolating the event titles and removing country identifiers.<br>
* **Dimensionality Reduction:** Drops unneeded attributes including `Athlete club`, `Athlete country`, `Athlete year of birth`, and `Athlete age category`.<br>
* **Data Integrity Checks:** Evaluates and removes rows with structural duplicate entries or missing numerical observations.<br>
* **Type Casting:** Converted `athlete age` into integers and `Athlete average speed` into float datatypes.<br>
* **Structuring:** Renames attributes using uniform snake_case notation and repositions columns to establish a clear logical hierarchy.<br>

### Key Insights and Metrics Showcased
The dashboard and notebook visually capture and demonstrate several underlying athletic trends:<br>
* **Race Distance Popularity:** A proportional distribution analysis matching total runner participation metrics across 50km and 50mi event lengths.<br>
* **Gender Demographics:** Quantified participation spreads between male and female athletes across distinct categories.<br>
* **Speed Discrepancy Analysis:** Metric evaluations mapping out the difference in average running speeds between male and female cohorts across both 50km and 50mi distances.<br>
* **Age vs. Speed Correlation:** Traces how runner speeds fluctuate across different life stages and helps answer how average age varies by race length.<br>
* **Course Difficulty Ranking:** Identifies the top 15 most grueling courses by isolating and sorting races with the lowest historical average athlete speeds.<br>
* **Seasonal Speed Performance:** Groups average performance speeds across different seasons and genders to pinpoint exactly which times of the year produce the fastest records.<br>
* **Race Competitiveness Profiling:** Leverages the mathematical concept of speed standard deviation to locate the 15 most competitive races, where a lower deviation indicates tightly contested close finishes.<br>

### Repository Components
* **marathon eda.ipynb:** The developmental notebook where data profiling, null handling, type corrections, column transformations, and primary charting are orchestrated.<br>
* **mar.py:** The interactive production script that converts the data architecture into a live Streamlit analytics presentation containing real-time filtering and high-performance Plotly charts.<br>
