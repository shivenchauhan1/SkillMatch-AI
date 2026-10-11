"""Local skill extraction and TF-IDF similarity utilities."""
import json, re
from pathlib import Path
from typing import Dict, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
ROOT = Path(__file__).resolve().parents[1]
def load_json(path):
    with path.open("r", encoding="utf-8") as f: return json.load(f)
def load_catalogues():
    return load_json(ROOT/"data"/"skill_catalogue.json"), load_json(ROOT/"data"/"role_catalogue.json")
def flatten_skills(catalogue: Dict[str,List[str]]) -> List[str]:
    values=set()
    for items in catalogue.values(): values.update(items)
    return sorted(values,key=lambda x:(-len(x),x))
def extract_skills(text, all_skills):
    normalized=(text or "").lower(); found=[]
    for skill in all_skills:
        pattern=r"(?<![a-z0-9+#])"+re.escape(skill.lower())+r"(?![a-z0-9+#])"
        if re.search(pattern,normalized): found.append(skill)
    return sorted(set(found))
def similarity_score(profile_text, role_text):
    texts=[(profile_text or "").strip(),(role_text or "").strip()]
    if not all(texts): return 0.0
    vec=TfidfVectorizer(stop_words="english",ngram_range=(1,2))
    matrix=vec.fit_transform(texts)
    return round(float(cosine_similarity(matrix[0:1],matrix[1:2])[0,0]*100),1)
def analyze_profile(profile_text, role_name, job_description=""):
    skills_cat, roles=load_catalogues()
    if role_name not in roles: raise ValueError(f"Unknown role: {role_name}")
    all_skills=flatten_skills(skills_cat); role=roles[role_name]
    role_text=role["description"]+" "+" ".join(role["required_skills"])+" "+(job_description or "")
    found=extract_skills(profile_text,all_skills); required=sorted(set(role["required_skills"]))
    matched=sorted(set(found).intersection(required)); missing=sorted(set(required).difference(found))
    return {"role":role_name,"recognized_skills":found,"required_skills":required,"matched_skills":matched,
    "missing_skills":missing,"skill_coverage":round(100*len(matched)/max(1,len(required)),1),
    "text_similarity":similarity_score(profile_text,role_text),"roadmap":role["roadmap"],
    "note":"Text similarity and skill coverage are descriptive signals, not hiring probabilities or validated measures of job performance."}
