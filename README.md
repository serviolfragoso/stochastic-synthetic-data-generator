# 🚗 Synthetic Data Generator & Workforce Simulation Engine

> An enterprise-grade, zero-backend data pipeline and stochastic simulation engine designed to generate realistic commercial panel datasets (3.9k+ records), modeling agent productivity, tenure curves, seasonal volatility, and workforce turnover.

---

## 🧭 Executive Summary & Business Context

In data science, analytics engineering, and business intelligence, having access to clean, realistic historical data for testing pipelines and dashboards is a constant bottleneck. Real corporate data is sensitive and proprietary, making portfolio-building difficult.

The idea is to create a synthetic data set where we can create for several years, N number of agents and their sales result each month, so we have 
* Starting month and year 
* Number of years to be simulated
* 4 regions 
* 2 sales channel 
* Sales success weight for each region and channel
* Agent tenure
* Tenure ramp up (affects sales resultos for new agents)
* Churn probability for each rep
* Monthly average sales per agent
* Number of agents to have in or pool each month

With this parameters we can create a data for the number of years to be simulated given by the user, the main idea is to be able to create N number of datasets to practice statics tools, forecasting, create dashboards or any task required by the user. 

This project solves this by implementing a **Stochastic Simulation Pipeline in Python**. It leverages statistical distributions (**Poisson** for transaction counts and **Lognormal** for skill variance) alongside actuarial churn matrices to generate a 36-month synthetic panel dataset. The pipeline automatically sanitizes and syncs data via Google Cloud Service Accounts to Google Sheets, powering a live executive dashboard in Looker Studio.

## 🏗️ System Architecture & Workflow

```text
[ config_reps.py ] (Parameters & Actuarial Assumptions)
        │
        ▼
[ datagenerator.py ] (NumPy Stochastic Simulation: Poisson, Lognormal, Churn)
        │
        ▼
[ gsheets_loader.py ] (Google Cloud IAM Service Account & gspread API Integration)
        │
        ▼
[ Google Sheets ] ──> [ Looker Studio Executive Dashboard ] (Live BI Consumption)
```

⚙️ Key Technical FeaturesStochastic Event Generation (Poisson Distribution): Transaction counts (sales_units) are modeled dynamically using a rate parameter ($\lambda_{it}$) that scales with individual skill, regional multipliers, annual seasonality factors, and tenure ramp-up curves.Actuarial Churn & Workforce Continuity: Implements a retention matrix based on tenure brackets (0-3 months, 4-12 months, 13+ months) to realistically simulate employee attrition and automated pipeline backfilling.Zero-Backend Cloud Sync: Seamlessly integrates with Google Sheets API using secure IAM credentials, updating raw data ranges programmatically without breaking upper-layer BI report connections.

📁 Repository Structure
revops-sales-forecasting-engine/

│

├── config_reps.py          # Centralized configuration (Seasonality, Churn matrix, Regions)

├── datagenerator.py        # Core simulation class (SalesForceSimulator) and NumPy logic

├── gsheets_loader.py       # Google Sheets API client and batch ingestion handler

├── requirements.txt        # Project dependencies (pandas, numpy, gspread, google-auth)

└── README.md               # Technical documentation

📊 Live Interactive Dashboards & Data Source
Looker Studio Executive Dashboard: View Live Looker Studio Report

Google Sheets Data Source (Sample): Explore Google Sheets Dataset

🛠️ Setup & Installation
1. Clone the Repository
git clone [https://github.com/serviolfragoso/revops-sales-forecasting-engine.git](https://github.com/serviolfragoso/stochastic-synthetic-data-generator.git)
cd revops-sales-forecasting-engine

2. Install Dependencies
Bash
pip install pandas numpy gspread google-auth

3. Configure Credentials
Place your Google Cloud Service Account JSON key in the root directory and name it service-account.json (Note: Excluded from version control via .gitignore).

4. Run the Simulation Pipeline
Bash
python datagenerator.py

📈 Design Decisions & Mathematical BreakdownWhy Poisson over Uniform/Normal? Sales counts are discrete, bounded at zero, and exhibit variance characteristics that fit counting processes well. The expected lambda($\lambda_{i,t}$ is mathematically derived as:


$\lambda_{i,t} = \text{Base} \times \text{Skill}_i \times \text{RegionMultiplier}_r \times \text{Seasonality}_t \times \text{RampUp}_m$

Lognormal Skill Distribution: Prevents negative skill weights while creating a realistic right-skewed performance distribution where a small percentage of agents significantly outperform the baseline.
