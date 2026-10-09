Markdown# 🚗 Stochastic Sales Force & Attrition Simulation Engine

> An enterprise-grade, zero-backend data pipeline and stochastic simulation engine designed to model sales force productivity, tenure dynamics, seasonal volatility, and human capital churn.

---

## 🧭 Executive Summary & Business Context
In commercial operations, forecasting sales without factoring in agent tenure curves, regional channel dynamics, and team turnover (*churn*) leads to severe financial miscalculations. 

This project implements a **Quantitative Sales Forecasting & Workforce Simulation Pipeline** in Python. It uses statistical distributions (**Poisson** for discrete transaction counts and **Lognormal** for individual skill variance) combined with actuarial churn matrices to generate a synthetic panel dataset over a 36-month horizon (~21,600 atomic records). The pipeline automatically sanitizes and syncs data to Google Sheets via Google Cloud Service Accounts, serving a live executive dashboard in Looker Studio.

---

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
⚙️ Key Technical FeaturesStochastic Event Generation (Poisson Distribution): Transaction counts ($sales\_units$) are modeled dynamically using a rate parameter ($\lambda_{it}$) that scales with individual skill, regional multipliers, annual seasonality factors, and tenure ramp-up curves.Actuarial Churn & Workforce Continuity: Implements a retention matrix based on tenure brackets (0-3 months, 4-12 months, 13+ months) to realistically simulate employee attrition and automated pipeline backfilling.Zero-Backend Cloud Sync: Seamlessly integrates with Google Sheets API using secure IAM credentials, updating raw data ranges programmatically without breaking upper-layer BI report connections.

📁 Repository StructurePlaintextrevops-sales-forecasting-engine/
│
├── config_reps.py          # Centralized configuration (Seasonality, Churn matrix, Regions)
├── datagenerator.py        # Core simulation class (SalesForceSimulator) and NumPy logic
├── gsheets_loader.py       # Google Sheets API client and batch ingestion handler
├── requirements.txt        # Project dependencies (pandas, numpy, gspread, google-auth)
└── README.md               # Technical documentation
📊 Live Interactive Dashboards & Data SourceLooker Studio Executive Dashboard: View Live Looker Studio ReportGoogle Sheets Data Source (Sample): Explore Google Sheets Dataset🛠️ Setup & Installation1. Clone the RepositoryBashgit clone [https://github.com/serviolfragoso/revops-sales-forecasting-engine.git](https://github.com/serviolfragoso/revops-sales-forecasting-engine.git)
cd revops-sales-forecasting-engine
2. Install DependenciesBashpip install pandas numpy gspread google-auth
3. Configure CredentialsPlace your Google Cloud Service Account JSON key in the root directory and name it service-account.json (Note: Excluded from version control via .gitignore).
4. Run the Simulation PipelineBashpython datagenerator.py
📈 Design Decisions & Mathematical Breakdown

* **Why Poisson over Uniform/Normal?** Sales counts are discrete, bounded at zero, and exhibit variance characteristics that fit counting processes well. The expected lambda ($\lambda_{it}$) is mathematically derived as:

```math
\lambda_{it} = \text{Base} \times \text{Skill}_i \times \text{RegionMultiplier} \times \text{Seasonality}_t \times \text{RampUp}(\text{Tenure})
Lognormal Skill Distribution: Prevents negative skill weights while creating a realistic right-skewed performance distribution where a small percentage of agents significantly outperform the baseline.
