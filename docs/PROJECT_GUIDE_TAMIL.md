# Project Guide — தமிழில்

## இந்த project என்ன செய்கிறது?
இந்த capstone-ல் நான்கு பகுதிகள் உள்ளன:
1. **Part A — Data Foundation:** CSV data உருவாக்குதல், clean செய்தல், SQLite database-ல் சேமித்தல், SQL query-கள்.
2. **Part B — Customer Segments and Lapse Prediction:** customer order history-இல் இருந்து features உருவாக்கி baseline ML model train/evaluate செய்தல்.
3. **Part C — Support Ticket Triage:** support message-ஐ category/priority-ஆக வகைப்படுத்தி safe next action பரிந்துரைத்தல்.
4. **Part D — Policy RAG Assistant and Refund Agent:** demo policy text-இல் இருந்து relevant passage retrieve செய்தல்; refund request-ஐ human review-க்கு route செய்தல்.

## VS Code-ல் தொடங்குவது
1. ZIP-ஐ extract செய்யவும்.
2. VS Code → **File → Open Folder** → `instamart_customer_intelligence_capstone` folder தேர்வு செய்யவும்.
3. **Terminal → New Terminal** திறக்கவும்.
4. கீழே உள்ள commands-ஐ ஒவ்வொன்றாக இயக்கவும்:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m src.generate_data
python -m src.run_pipeline
```

5. ML model:
```powershell
python -m src.train_lapse_model
```
6. Ticket triage:
```powershell
python -m src.ticket_triage
```
7. Refund agent:
```powershell
python -m src.refund_agent
```
8. Dashboard:
```powershell
streamlit run app.py
```

## Output எங்கே வரும்?
- `data/generated/` — synthetic customers/orders/tickets CSV.
- `data/instamart_demo.db` — SQLite database.
- `outputs/data_quality_summary.csv` — data quality summary.
- `outputs/monthly_revenue.csv` — monthly summary.
- `outputs/lapse_model_report.txt` — ML evaluation.
- `outputs/ticket_triage_results.csv` — ticket triage results.

## முக்கியமான குறிப்பு
இந்த data முழுவதும் practice-க்காக உருவாக்கப்பட்டது; உண்மையான Instamart customer data அல்ல. Refund agent எந்த உண்மையான refund-ஐயும் process செய்யாது. Lapse prediction demo-வை உண்மையான customer decisions-க்கு பயன்படுத்தக் கூடாது. இந்த starter kit-ஐ உங்கள் PDF rubric-ல் உள்ள exact deliverables, screenshots, README, GitHub submission விதிகளுடன் ஒப்பிட்டு இறுதியாக மாற்றவும்.
