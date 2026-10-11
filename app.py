import streamlit as st
import pandas as pd
from src.matcher import analyze_profile, load_catalogues
st.set_page_config(page_title="SkillMatch AI",page_icon="🎯",layout="wide")
st.title("🎯 SkillMatch AI")
st.subheader("Career skill-gap analyzer")
st.write("Compare your current skills with a target role, identify gaps, and get a practical learning roadmap.")
st.info("Educational prototype: scores reflect catalogue matches and text similarity, not a probability of getting hired.")
_, roles=load_catalogues()
with st.sidebar:
    st.header("Your target")
    role_name=st.selectbox("Choose a target role",list(roles.keys()))
    st.caption("Optionally paste a job description to tailor the text comparison.")
example="Python, SQL, pandas, NumPy, Excel, data cleaning, statistics, Git, communication, and problem solving. I have built a dashboard project and practiced exploratory data analysis."
profile=st.text_area("Your skills and experience",value=example,height=150,placeholder="Enter skills, tools, courses, projects, and experience...")
job_description=st.text_area("Optional job description",height=130,placeholder="Paste a job description here (optional)...")
if st.button("Analyze my skill gap",type="primary",use_container_width=True):
    if not profile.strip(): st.error("Please enter skills or experience before analyzing.")
    else: st.session_state["result"]=analyze_profile(profile,role_name,job_description)
result=st.session_state.get("result")
if result:
    st.divider(); st.header("Your analysis: "+result["role"])
    c1,c2,c3=st.columns(3)
    c1.metric("Required skills matched",f'{len(result["matched_skills"])}/{len(result["required_skills"])}')
    c2.metric("Skill coverage",f'{result["skill_coverage"]:.1f}%')
    c3.metric("Text similarity",f'{result["text_similarity"]:.1f}/100')
    st.caption("Similarity measures text overlap; skill coverage counts recognized catalogue matches. Neither is a hiring probability.")
    left,right=st.columns(2)
    with left:
        st.subheader("Matched skills")
        if result["matched_skills"]:
            for skill in result["matched_skills"]: st.success(skill)
        else: st.write("No required skills recognized yet. Try adding specific tools or skills.")
    with right:
        st.subheader("Skills to develop")
        if result["missing_skills"]:
            for skill in result["missing_skills"]: st.warning(skill)
        else: st.success("All catalogue-listed skills were recognized in your profile.")
    st.subheader("Skill coverage")
    st.bar_chart(pd.DataFrame({"Skills":[len(result["matched_skills"]),len(result["missing_skills"])]},index=["Matched","Not listed"]))
    st.subheader("Suggested learning roadmap")
    for i,item in enumerate(result["roadmap"],1): st.markdown(f"**Step {i}.** {item}")
    report={"target_role":result["role"],"recognized_skills":", ".join(result["recognized_skills"]),"matched_skills":", ".join(result["matched_skills"]),"missing_skills":", ".join(result["missing_skills"]),"skill_coverage_percent":result["skill_coverage"],"text_similarity_score":result["text_similarity"],"interpretation":result["note"]}
    st.download_button("Download analysis as CSV",pd.DataFrame([report]).to_csv(index=False),file_name="skillmatch_analysis.csv",mime="text/csv")
    st.download_button("Download roadmap as TXT","\n".join(f"{i}. {x}" for i,x in enumerate(result["roadmap"],1)),file_name="skillmatch_roadmap.txt",mime="text/plain")
with st.expander("How this prototype works"):
    st.markdown("1. A local catalogue recognizes skill terms.\n2. TF-IDF and cosine similarity compare profile text with role text.\n3. Catalogue gaps and a curated roadmap are shown.\n\n**Limitations:** the catalogue is small and hand-curated; synonyms may be missed; the tool does not verify proficiency or predict hiring outcomes.")
st.caption("No paid API, external dataset download, login, or secrets required.")
