# Smart Agriculture Intelligence System

## 1. Overview

The Smart Agriculture Intelligence System is a beginner-level data analytics project that analyzes farmer activities, agricultural complaints, and crop-related information.

The project demonstrates the use of Python, SQL, Machine Learning, and Streamlit to support agricultural data analysis.

**Demo Dataset:**
- Farmers: 300
- Farm Activities: 1,800
- Farmer Complaints: 500

**Data Note:** This project uses synthetic demonstration data. It does not use official government data or real farmer records.

## 2. Reproduce

### Requirements
- Python 3.10 or above
- VS Code
- Required Python packages listed in `requirements.txt`

### Installation

```bash
pip install -r requirements.txt
```

### Generate Demo Data

```bash
python -m src.generate_data
```

### Run Data Pipeline

```bash
python -m src.run_pipeline
```

### Train Farmer Inactivity Model

```bash
python -m src.train_lapse_model
```

### Run Complaint Classification

```bash
python -m src.ticket_triage
```

### Run Farmer Support Agent

```bash
python -m src.refund_agent
```

### Run Agriculture Knowledge Assistant

```bash
python -m src.rag_assistant
```

### Run SQL Analysis

```bash
python run_sql.py
```

### Run Dashboard

```bash
streamlit run app.py
```

## 3. Part A — Data Foundation and SQL Analysis

This module generates and processes synthetic farmer, farm activity, and complaint datasets.

SQL analysis includes:
- Farmer-wise activity analysis
- Complaint category analysis
- Monthly farm activity value
- Farmer activity segmentation
- Crop-wise activity analysis

The data pipeline stores processed data in an SQLite database.

## 4. Part B — Farmer Inactivity Prediction

A baseline Machine Learning classification model is trained to demonstrate farmer inactivity prediction.

The model achieved:
- Accuracy: 0.47
- ROC-AUC: 0.466

These results show that the current model needs improvement. It is an educational baseline and should not be used for real-world farmer decisions.

## 5. Part C — Farmer Complaint Classification

The complaint classification module categorizes farmer complaints and suggests priority levels and recommended actions.

Example categories:
- Crop disease
- Payment issue
- Fertilizer query
- Other agricultural complaints

Complaints requiring expert attention are referred for human review.

## 6. Part D — Agriculture Knowledge Assistant and Support Agent

The project includes:
- A simple keyword-based knowledge retrieval prototype
- A farmer support assessment module
- Expert referral guidance for crop disease or pest complaints

The knowledge assistant uses a local demo knowledge file. It is not an external LLM and does not provide professional agricultural advice.

## 7. Limitations

- The datasets are synthetic and created for demonstration.
- The project does not use official government agricultural records.
- The inactivity model has low evaluation performance.
- The knowledge assistant uses simple retrieval and is not an advanced LLM.
- Outputs must not be treated as real agricultural recommendations.

## 8. Next Steps

- Integrate verified government agricultural datasets.
- Improve data quality and model performance.
- Add more crop and soil information.
- Improve the knowledge base with verified agricultural resources.
- Test the system using real-world data with appropriate permission.

## 9. Conclusion

This project demonstrates how data analytics, SQL, Machine Learning, and dashboard visualization can be combined in a Smart Agriculture application. It provides an educational foundation for further development.