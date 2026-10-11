from __future__ import annotations

import html
from pathlib import Path

import pandas as pd
import streamlit as st

from src.matcher import analyze_profile, load_catalogues


# -----------------------------------------------------------------------------
# Page setup and visual system
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="SkillMatch AI | Career Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

      :root {
        --sm-ink: #17213b;
        --sm-muted: #68738b;
        --sm-purple: #6558d9;
        --sm-purple-dark: #4b3fc1;
        --sm-line: #e5e9f3;
        --sm-panel: #ffffff;
        --sm-page: #f5f7fc;
        --sm-green: #16856b;
        --sm-red: #b94b5e;
      }
      html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
      .stApp { background: var(--sm-page); color: var(--sm-ink); }
      [data-testid="stHeader"] { background: rgba(245,247,252,.88); }
      [data-testid="stToolbar"] { right: 1rem; }
      .block-container { max-width: 1380px; padding-top: 1.55rem; padding-bottom: 3rem; }
      [data-testid="stSidebar"] { background: #fff; border-right: 1px solid var(--sm-line); }
      [data-testid="stSidebar"] > div:first-child { padding-top: 1.25rem; }
      [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: var(--sm-muted); }
      h1, h2, h3 { font-family: 'Manrope', sans-serif !important; color: var(--sm-ink); letter-spacing: -.035em; }
      h2 { font-size: 1.42rem !important; }
      h3 { font-size: 1.04rem !important; letter-spacing: -.02em; }
      p, label, li { color: var(--sm-muted); }
      div[data-testid="stTextArea"] textarea, div[data-testid="stTextInput"] input {
        border: 1px solid #dfe4f0; border-radius: 12px; background: #fbfcff;
        color: var(--sm-ink); line-height: 1.55; padding: .8rem .9rem;
      }
      div[data-testid="stTextArea"] textarea:focus, div[data-testid="stTextInput"] input:focus {
        border-color: #8a80eb; box-shadow: 0 0 0 2px rgba(101,88,217,.12);
      }
      div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        border-color: #dfe4f0; border-radius: 11px; background: #fbfcff;
      }
      .stButton > button, .stDownloadButton > button, [data-testid="stFormSubmitButton"] button {
        border-radius: 11px; font-weight: 700; min-height: 2.8rem;
        transition: transform .15s ease, box-shadow .15s ease;
      }
      [data-testid="stFormSubmitButton"] button, .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #7064e8 0%, #5548cb 100%);
        border: 0; color: white; box-shadow: 0 7px 16px rgba(86,72,203,.18);
      }
      [data-testid="stFormSubmitButton"] button:hover, .stButton > button[kind="primary"]:hover {
        box-shadow: 0 10px 22px rgba(86,72,203,.24); transform: translateY(-1px);
      }
      .stDownloadButton > button { background: white; border: 1px solid var(--sm-line); color: var(--sm-ink); }
      [data-testid="stMetric"] { background: #fff; border: 1px solid var(--sm-line); border-radius: 16px; padding: 1.05rem 1.1rem; box-shadow: 0 4px 14px rgba(26,40,78,.025); }
      [data-testid="stMetricLabel"] p { font-size: .78rem; font-weight: 700; text-transform: uppercase; letter-spacing: .065em; color: var(--sm-muted); }
      [data-testid="stMetricValue"] { color: var(--sm-ink); font-family: 'Manrope', sans-serif; letter-spacing: -.04em; }
      [data-testid="stProgressBar"] > div { background: #e7e9f6; border-radius: 999px; height: .6rem; }
      [data-testid="stProgressBar"] > div > div { background: linear-gradient(90deg, #8276ee, #5548cb); border-radius: 999px; }
      [data-testid="stVerticalBlockBorderWrapper"] { border-color: var(--sm-line) !important; border-radius: 17px !important; background: white; }
      [data-testid="stExpander"] { border-color: var(--sm-line); border-radius: 13px; background: white; }
      hr { border-color: var(--sm-line); }
      .sm-brand { display:flex; align-items:center; gap:.7rem; margin:.1rem 0 1.1rem; }
      .sm-logo { width:42px; height:42px; display:flex; align-items:center; justify-content:center; color:#fff; border-radius:14px; font-size:1.3rem; font-weight:800; background:linear-gradient(135deg,#8276ef,#5143c3); box-shadow:0 7px 15px rgba(86,72,203,.23); }
      .sm-brand-name { font-family:'Manrope',sans-serif; font-size:1.13rem; font-weight:800; color:var(--sm-ink); letter-spacing:-.04em; line-height:1.2; }
      .sm-brand-sub { font-size:.72rem; color:var(--sm-muted); margin-top:.2rem; }
      .sm-hero { padding:1.6rem 1.7rem 1.55rem; background:linear-gradient(112deg,#fff 0%,#fff 54%,#f0efff 100%); border:1px solid var(--sm-line); border-radius:22px; box-shadow:0 7px 22px rgba(25,39,82,.035); margin-bottom:1.35rem; }
      .sm-eyebrow { text-transform:uppercase; letter-spacing:.13em; font-size:.69rem; font-weight:800; color:var(--sm-purple); margin-bottom:.55rem; }
      .sm-hero-title { font-family:'Manrope',sans-serif; font-size:clamp(1.7rem, 3.3vw, 2.55rem); letter-spacing:-.055em; line-height:1.1; font-weight:800; color:var(--sm-ink); margin:0 0 .6rem; }
      .sm-hero-copy { font-size:.97rem; line-height:1.6; max-width:720px; color:var(--sm-muted); margin:0; }
      .sm-pills { display:flex; flex-wrap:wrap; gap:.45rem; margin-top:1rem; }
      .sm-pill { display:inline-flex; align-items:center; gap:.35rem; border-radius:999px; background:#f1f0ff; color:#5145bf; font-size:.73rem; font-weight:700; padding:.42rem .7rem; border:1px solid #e4e0ff; }
      .sm-section-kicker { font-size:.72rem; text-transform:uppercase; letter-spacing:.11em; color:var(--sm-purple); font-weight:800; margin-bottom:.3rem; }
      .sm-muted-note { color:var(--sm-muted); font-size:.85rem; line-height:1.55; }
      .sm-mini-card { border:1px solid var(--sm-line); border-radius:15px; background:#fff; padding:1rem; height:100%; }
      .sm-mini-icon { width:32px; height:32px; display:flex; align-items:center; justify-content:center; border-radius:10px; background:#f0efff; color:var(--sm-purple); font-size:1rem; margin-bottom:.65rem; }
      .sm-mini-title { font-family:'Manrope',sans-serif; font-weight:800; color:var(--sm-ink); font-size:.9rem; margin-bottom:.3rem; }
      .sm-mini-copy { color:var(--sm-muted); font-size:.79rem; line-height:1.55; }
      .sm-panel-title { font-family:'Manrope',sans-serif; font-size:1.05rem; font-weight:800; letter-spacing:-.025em; color:var(--sm-ink); margin-bottom:.2rem; }
      .sm-panel-copy { color:var(--sm-muted); font-size:.82rem; line-height:1.5; }
      .sm-chip-wrap { display:flex; flex-wrap:wrap; gap:.5rem; padding:.25rem 0 .35rem; }
      .sm-chip { display:inline-flex; border:1px solid #d9f0e8; background:#eefaf5; color:#17745f; padding:.42rem .7rem; border-radius:9px; font-size:.79rem; font-weight:700; }
      .sm-chip-missing { border-color:#f3dce2; background:#fff2f4; color:#a84257; }
      .sm-empty-chip { color:var(--sm-muted); font-size:.86rem; padding:.2rem 0; }
      .sm-roadmap { border:1px solid var(--sm-line); border-radius:14px; padding:.95rem 1rem; margin-bottom:.65rem; background:#fff; display:flex; gap:.8rem; align-items:flex-start; }
      .sm-roadmap-num { min-width:30px; height:30px; border-radius:10px; background:#f0efff; color:var(--sm-purple); font-weight:800; display:flex; align-items:center; justify-content:center; font-size:.82rem; }
      .sm-roadmap-text { color:#35405a; line-height:1.55; font-size:.9rem; padding-top:.25rem; }
      .sm-footer { border-top:1px solid var(--sm-line); padding-top:1.1rem; margin-top:2rem; font-size:.75rem; line-height:1.6; color:#8690a6; }
      .sm-sidebar-note { border:1px solid var(--sm-line); border-radius:13px; padding:.9rem; background:#fafbff; font-size:.81rem; color:var(--sm-muted); line-height:1.55; }
      @media (max-width: 800px) { .block-container { padding-left:1rem; padding-right:1rem; } .sm-hero { padding:1.2rem; } }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------------------------------------------------------
# Load the project catalogues
# -----------------------------------------------------------------------------
try:
    skill_catalogue, roles = load_catalogues()
except Exception as exc:  # show a useful message if the deployed repo misses data/src
    st.error("SkillMatch AI couldn't load its local catalogues. Check that the `src/` and `data/` folders are in the GitHub repository.")
    st.exception(exc)
    st.stop()

role_names = list(roles.keys())
example_profile = (
    "I am a third-year B.Tech Computer Science student with knowledge of Python, SQL, "
    "pandas, NumPy, Excel, data cleaning, statistics, data visualization, Git, "
    "communication, and problem solving. I have built a dashboard project and practiced "
    "exploratory data analysis."
)

if "sm_profile_text" not in st.session_state:
    st.session_state.sm_profile_text = example_profile
if "sm_job_description" not in st.session_state:
    st.session_state.sm_job_description = ""
if "sm_target_role" not in st.session_state:
    st.session_state.sm_target_role = role_names[0] if role_names else ""
if "sm_result" not in st.session_state:
    st.session_state.sm_result = None


# -----------------------------------------------------------------------------
# Sidebar
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="sm-brand">
          <div class="sm-logo">S</div>
          <div><div class="sm-brand-name">SkillMatch AI</div><div class="sm-brand-sub">Career insights workspace</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("### Your workspace")
    st.markdown("Use your current skills to explore gaps for a role you want to pursue.")
    st.markdown("---")
    st.markdown("**A simple workflow**")
    st.markdown("1. Add skills, tools, projects, and experience.\n2. Choose a target role.\n3. Review skill gaps and your learning plan.")
    st.markdown("---")
    st.markdown(
        "<div class='sm-sidebar-note'><b>Privacy-first prototype</b><br>No account, API key, or external dataset is required. Avoid entering personal contact details or other sensitive information.</div>",
        unsafe_allow_html=True,
    )
    st.markdown(" ")
    if st.button("Reset to sample profile", use_container_width=True):
        st.session_state.sm_profile_text = example_profile
        st.session_state.sm_job_description = ""
        st.session_state.sm_target_role = role_names[0] if role_names else ""
        st.session_state.sm_result = None
        st.rerun()


# -----------------------------------------------------------------------------
# Page header
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="sm-hero">
      <div class="sm-eyebrow">Your career, made more actionable</div>
      <div class="sm-hero-title">Find your next skill to build.</div>
      <p class="sm-hero-copy">Map your current experience against a target role, uncover catalogue-listed skill gaps, and turn the results into a practical learning plan.</p>
      <div class="sm-pills">
        <span class="sm-pill">✦ Skill gap analysis</span>
        <span class="sm-pill">↗ Role-focused roadmap</span>
        <span class="sm-pill">● No paid API required</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Input workspace
st.markdown('<div class="sm-section-kicker">01 / Build your profile</div>', unsafe_allow_html=True)
st.markdown("## Start with what you know")
st.markdown(
    '<p class="sm-muted-note">Include technical skills, tools, coursework, personal projects, internships, and transferable skills. Specific terms help the prototype recognise your experience.</p>',
    unsafe_allow_html=True,
)

with st.form("sm_analysis_form", clear_on_submit=False):
    profile_col, context_col = st.columns([1.55, 1], gap="large")

    with profile_col:
        st.text_area(
            "Your skills and experience",
            key="sm_profile_text",
            height=250,
            placeholder="Example: Python, SQL, Power BI, data cleaning... Describe projects and experience too.",
            help="Write naturally or use a comma-separated list. The tool recognises phrases from its built-in catalogue.",
        )
        current_text = st.session_state.get("sm_profile_text", "")
        st.caption(f"{len(current_text):,} characters · Avoid including phone numbers, email addresses, or other sensitive details.")

    with context_col:
        st.markdown(
            '<div class="sm-panel-title">Choose a target</div><div class="sm-panel-copy">Compare your profile with a role from the project catalogue.</div>',
            unsafe_allow_html=True,
        )
        st.selectbox("Target role", options=role_names, key="sm_target_role", help="Each role uses a small curated list of required skills.")
        with st.expander("Add a specific job description (optional)", expanded=False):
            st.text_area(
                "Job description",
                key="sm_job_description",
                height=155,
                placeholder="Paste the responsibilities and requirements from a job or internship listing...",
                help="The text is used for similarity comparison. It does not change the curated missing-skills list.",
            )
        st.markdown(
            "<div class='sm-sidebar-note'><b>What you will get</b><br>Recognised skills, matched and missing role skills, a text-overlap score, and a suggested learning roadmap.</div>",
            unsafe_allow_html=True,
        )

    submitted = st.form_submit_button("Analyse my profile  →", use_container_width=True, type="primary")

if submitted:
    profile = st.session_state.get("sm_profile_text", "")
    target_role = st.session_state.get("sm_target_role", role_names[0] if role_names else "")
    job_description = st.session_state.get("sm_job_description", "")
    if not profile.strip():
        st.session_state.sm_result = None
        st.error("Add some skills or experience before running the analysis.")
    else:
        try:
            st.session_state.sm_result = analyze_profile(profile, target_role, job_description)
        except Exception as exc:
            st.error("The analysis couldn't be completed. Please check the inputs and try again.")
            st.exception(exc)


# -----------------------------------------------------------------------------
# Analysis result
# -----------------------------------------------------------------------------
result = st.session_state.get("sm_result")
if not result:
    st.markdown(" ")
    st.markdown('<div class="sm-section-kicker">02 / Your workflow</div>', unsafe_allow_html=True)
    cards = st.columns(3, gap="medium")
    card_content = [
        ("01", "Map your strengths", "See which skills from the built-in catalogue are recognised in your profile."),
        ("02", "Spot the gaps", "Compare recognised skills against the target role's curated requirements."),
        ("03", "Take the next step", "Use a practical roadmap to decide what to practise or build next."),
    ]
    for col, (number, title, copy) in zip(cards, card_content):
        with col:
            st.markdown(
                f"<div class='sm-mini-card'><div class='sm-mini-icon'>{html.escape(number)}</div><div class='sm-mini-title'>{html.escape(title)}</div><div class='sm-mini-copy'>{html.escape(copy)}</div></div>",
                unsafe_allow_html=True,
            )
else:
    st.markdown(" ")
    st.markdown('<div class="sm-section-kicker">02 / Your results</div>', unsafe_allow_html=True)
    st.markdown(f"## Skill match snapshot · {html.escape(result['role'])}")
    st.markdown(
        '<p class="sm-muted-note">These figures describe recognised catalogue matches and text overlap. They are not a hiring score or a measure of your actual proficiency.</p>',
        unsafe_allow_html=True,
    )

    metric1, metric2, metric3 = st.columns(3, gap="medium")
    metric1.metric("Required skills matched", f"{len(result['matched_skills'])} / {len(result['required_skills'])}")
    metric2.metric("Skill coverage", f"{result['skill_coverage']:.1f}%")
    metric3.metric("Text similarity", f"{result['text_similarity']:.1f} / 100")

    st.markdown(" ")
    coverage_col, context_info_col = st.columns([1.3, 1], gap="large")
    with coverage_col:
        st.markdown('<div class="sm-panel-title">Role skill coverage</div>', unsafe_allow_html=True)
        st.progress(max(0, min(100, int(round(result["skill_coverage"])))) / 100)
        st.markdown(
            f'<p class="sm-muted-note">{len(result["matched_skills"])} of {len(result["required_skills"])} skills listed for this role were recognised in your profile.</p>',
            unsafe_allow_html=True,
        )
    with context_info_col:
        st.markdown(
            '<div class="sm-sidebar-note"><b>How to interpret this</b><br>Coverage is based on exact phrase recognition against a small catalogue. Similarity uses TF-IDF and cosine similarity to compare text. Neither score estimates hiring probability.</div>',
            unsafe_allow_html=True,
        )

    st.markdown(" ")
    matched_col, missing_col = st.columns(2, gap="large")
    with matched_col:
        with st.container(border=True):
            st.markdown('<div class="sm-panel-title">✓ Skills recognised</div>', unsafe_allow_html=True)
            st.markdown('<div class="sm-panel-copy">Role requirements found in your profile text.</div>', unsafe_allow_html=True)
            if result["matched_skills"]:
                chips = "".join(f"<span class='sm-chip'>{html.escape(skill)}</span>" for skill in result["matched_skills"])
                st.markdown(f"<div class='sm-chip-wrap'>{chips}</div>", unsafe_allow_html=True)
            else:
                st.markdown('<div class="sm-empty-chip">No required skills were recognised yet. Add specific skill names and try again.</div>', unsafe_allow_html=True)
    with missing_col:
        with st.container(border=True):
            st.markdown('<div class="sm-panel-title">＋ Skills to explore</div>', unsafe_allow_html=True)
            st.markdown('<div class="sm-panel-copy">Role requirements not recognised in your profile text.</div>', unsafe_allow_html=True)
            if result["missing_skills"]:
                chips = "".join(f"<span class='sm-chip sm-chip-missing'>{html.escape(skill)}</span>" for skill in result["missing_skills"])
                st.markdown(f"<div class='sm-chip-wrap'>{chips}</div>", unsafe_allow_html=True)
            else:
                st.markdown('<div class="sm-empty-chip">All catalogue-listed required skills were recognised. Consider checking the role description for additional requirements.</div>', unsafe_allow_html=True)

    st.markdown(" ")
    st.markdown('<div class="sm-section-kicker">03 / Your learning plan</div>', unsafe_allow_html=True)
    st.markdown("## A roadmap you can act on")
    st.markdown('<p class="sm-muted-note">Use these as suggested practice steps. Prioritise based on the job description, your interests, and the time you have available.</p>', unsafe_allow_html=True)
    for index, item in enumerate(result["roadmap"], start=1):
        st.markdown(
            f"<div class='sm-roadmap'><div class='sm-roadmap-num'>{index:02d}</div><div class='sm-roadmap-text'>{html.escape(item)}</div></div>",
            unsafe_allow_html=True,
        )

    report = {
        "target_role": result["role"],
        "recognized_skills": ", ".join(result["recognized_skills"]),
        "matched_skills": ", ".join(result["matched_skills"]),
        "missing_skills": ", ".join(result["missing_skills"]),
        "required_skill_count": len(result["required_skills"]),
        "skill_coverage_percent": result["skill_coverage"],
        "text_similarity_score": result["text_similarity"],
        "interpretation": result["note"],
    }
    csv_bytes = pd.DataFrame([report]).to_csv(index=False).encode("utf-8")
    roadmap_text = "SkillMatch AI — Learning Roadmap\n"
    roadmap_text += f"Target role: {result['role']}\n\n"
    roadmap_text += "Suggested steps:\n"
    roadmap_text += "\n".join(f"{i}. {step}" for i, step in enumerate(result["roadmap"], start=1))
    roadmap_text += "\n\nNote: This is an educational prototype, not a hiring prediction.\n"

    st.markdown(" ")
    download_col1, download_col2, _ = st.columns([1, 1, 2], gap="medium")
    with download_col1:
        st.download_button(
            "Download analysis · CSV",
            data=csv_bytes,
            file_name="skillmatch_analysis.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with download_col2:
        st.download_button(
            "Download roadmap · TXT",
            data=roadmap_text,
            file_name="skillmatch_roadmap.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with st.expander("How SkillMatch AI works — and its limitations"):
        st.markdown(
            """
            1. **Skill recognition:** searches your profile for phrases in a local, curated skill catalogue.
            2. **Role comparison:** compares recognised skills with the selected role's required-skill list.
            3. **Text similarity:** uses TF-IDF and cosine similarity to estimate textual overlap between your profile and role description.
            4. **Learning roadmap:** displays curated practice steps associated with that role.

            **Limitations:** the catalogue is small and may miss synonyms or relevant skills. Recognising a term does not verify proficiency. Text similarity is not a hiring probability, and this prototype should support—not replace—your own judgement.
            """
        )

st.markdown(
    "<div class='sm-footer'>SkillMatch AI · Educational career-planning prototype · Local catalogue-based analysis<br>Built to help learners reflect on skills and plan practice. Results are indicative, not validated assessments of competence or employability.</div>",
    unsafe_allow_html=True,
)
