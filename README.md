# SkillMatch AI
A lightweight, local-first career skill-gap analyzer for the IBM SkillsBuild AICTE Machine Learning & Applied AI internship project.

## Features
- Student-entered skills and optional job description.
- Local skill phrase recognition from a bundled JSON catalogue.
- TF-IDF + cosine similarity for text overlap.
- Matched/missing skills, catalogue coverage, and curated role learning roadmap.
- CSV report and TXT roadmap downloads.
- Five role templates: Data Analyst, Machine Learning Intern, Data Scientist, Frontend Developer, Backend Developer.

## Interpretation and limitations
Text similarity is not hiring probability. Skill coverage counts recognized terms from a small curated role catalogue; it does not verify competence. Synonyms and requirements can be missed. This is an educational prototype, not a hiring decision tool. Avoid entering sensitive personal information.

## Requirements
Python 3.10+ (3.10–3.12 recommended). No external API or runtime dataset download.

## Run locally — Windows PowerShell
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m streamlit run app.py
```
If activation is blocked:
```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

## Run locally — macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Test
```bash
python -m unittest discover -s tests
```

## Deploy afterward: Streamlit Community Cloud
1. Push this folder's contents to a GitHub repository.
2. Ensure `app.py`, `requirements.txt`, `src/`, and `data/` are at repository root.
3. Create an app in Streamlit Community Cloud and choose `app.py` as the main file.
4. Deploy; no secrets/API keys are needed.
5. Test the deployed app in a fresh browser session.
