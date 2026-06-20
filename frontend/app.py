import streamlit as st
import time
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.manager_agent import ManagerAgent
from core.config import settings

st.set_page_config(page_title="CodeMentor AI | Top 1% Edition", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

st.markdown(\"\"\"
    <style>
        .main { background-color: #0b0f19; color: #f2f5fa; font-family: 'Inter', sans-serif; }
        .stButton>button { background: linear-gradient(90deg, #bb86fc 0%, #7e57c2 100%); color: white; border-radius: 12px; border: none; padding: 12px 24px; font-weight: bold; width: 100%; transition: all 0.3s cubic-bezier(.25,.8,.25,1); }
        .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(187, 134, 252, 0.4); }
        .glass-panel { background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(10px); border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); padding: 20px; margin-bottom: 20px; }
        .header-title { background: -webkit-linear-gradient(45deg, #00f2fe, #bb86fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 900; font-size: 3rem; margin-bottom: 0px; }
    </style>
\"\"\", unsafe_allow_html=True)

if "session_history" not in st.session_state:
    st.session_state["session_history"] = []

@st.cache_resource
def get_manager():
    return ManagerAgent()

manager = get_manager()

def log_session(task: str, result: dict):
    st.session_state["session_history"].append({"task": task, "time": time.strftime('%H:%M:%S'), "result": result})

def download_report_button(result: dict, filename="report.json"):
    data = json.dumps(result, indent=2)
    st.download_button(label="📥 Download Report", data=data, file_name=filename, mime="application/json")

def render_pipeline_execution(task_name: str, **kwargs):
    final_res = None
    with st.status("Initializing Multi-Agent Pipeline...", expanded=True) as status:
        for event in manager.run_pipeline(task_name, **kwargs):
            if "status" in event and event["status"] == "thinking":
                st.write(f"🔄 {event['message']}")
            elif "status" in event and event["status"] == "complete":
                final_res = event.get("result")
                status.update(label="Pipeline Execution Complete!", state="complete", expanded=False)
            elif "error" in event:
                status.update(label="Pipeline Failed", state="error")
                st.error(event["error"])
                return None
    if final_res:
        log_session(task_name, final_res)
    return final_res

def draw_sidebar():
    with st.sidebar:
        st.markdown("<h2 style='color:#00f2fe'>CodeMentor V2</h2>", unsafe_allow_html=True)
        st.caption("Advanced Agentic Reasoning System")
        st.divider()
        st.write("### Firewall Status")
        st.write("🟢 Security Core: Active")
        st.write("🟢 Payload Limiter: Active")
        st.divider()
        st.write("### Session History")
        if st.session_state["session_history"]:
            for item in st.session_state["session_history"]:
                st.caption(f"[{item['time']}] - {item['task'].upper()}")
        else:
            st.caption("No history yet.")

def page_home():
    st.markdown("<h1 class='header-title'>CodeMentor AI V2</h1>", unsafe_allow_html=True)
    st.markdown(\"\"\"
    <div class='glass-panel'>
    <h3>Welcome to the Top 1% Kaggle Submission.</h3>
    Unlike standard GPT interfaces, CodeMentor AI processes tasks through a <b>Multi-Stage Verification Pipeline</b> to actively squash hallucinations.
    </div>
    \"\"\", unsafe_allow_html=True)

def page_solve():
    st.header("🧠 Advanced Solver Pipeline (Solve->Reflect->Verify->QA)")
    prob = st.text_area("Problem Statement:", height=150)
    if st.button("Engage Pipeline"):
        if prob:
            res = render_pipeline_execution("solve_pipeline", problem_statement=prob)
            if res:
                download_report_button(res, "solver_report.json")
                st.success("Verified Result Rendered")
                st.markdown("### 💬 Mentor Notes")
                st.info(res.get("final_explanation", ""))
                st.markdown("### 💻 Verified Code")
                st.code(res.get("final_code", ""), language="python")

def page_interview():
    st.header("👔 Staff FAANG Interviewer")
    col1, col2 = st.columns(2)
    with col1: prob = st.text_area("What problem are you solving?", height=150)
    with col2: code = st.text_area("Your thought process / code so far:", height=150)
    if st.button("Ask Interviewer"):
        if prob and code:
            res = render_pipeline_execution("interview", problem_statement=prob, user_code=code)
            if res:
                download_report_button(res, "interview_report.json")
                st.warning(res.get("feedback", ""))
                st.info(res.get("probing_question", ""))

def page_review():
    st.header("🔎 Code Reviewer (Strict Mode)")
    code = st.text_area("Paste code for style/PR review:", height=200)
    if st.button("Submit PR Review"):
        if code:
            res = render_pipeline_execution("review", code=code)
            if res:
                download_report_button(res, "review_report.json")
                st.metric("Style Score", f"{res.get('overall_score')}/10")
                for nit in res.get("comments", []): st.warning(f"**{nit.get('line_reference')}**: {nit.get('comment')}")
                st.code(res.get("refactored_snippet"), language="python")

def page_company():
    st.header("🏢 Company-Specific Review")
    company = st.selectbox("Target Company", ["Google", "Meta", "Amazon", "Netflix", "Apple", "Microsoft"])
    code = st.text_area("Paste code:", height=200)
    if st.button("Analyze Culture Fit"):
        if code:
            res = render_pipeline_execution("company", company_name=company, code=code)
            if res:
                download_report_button(res, "company_report.json")
                st.info(res.get("cultural_fit_advice", ""))
                st.warning(res.get("expected_follow_ups", ""))
                st.code(res.get("refactored_for_company", ""), language="python")

def page_hidden():
    st.header("🥷 Hidden Test Case Discovery")
    code = st.text_area("Paste code to find its vulnerabilities:", height=200)
    if st.button("Find Hidden Traps"):
        if code:
            res = render_pipeline_execution("hidden_test", code=code)
            if res:
                download_report_button(res, "hidden_tests.json")
                st.metric("Vulnerability Score", f"{res.get('vulnerability_score')}/10")
                for trap in res.get("discovered_traps", []): st.error(f"{trap.get('trap_name')} -> Input: {trap.get('trigger_input')}")

def main():
    draw_sidebar()
    tabs = st.tabs(["🏠 Home", "🧠 Pipeline", "👔 Mock", "🔎 Code Review", "🏢 Culture Fit", "🥷 Hidden Tests"])
    with tabs[0]: page_home()
    with tabs[1]: page_solve()
    with tabs[2]: page_interview()
    with tabs[3]: page_review()
    with tabs[4]: page_company()
    with tabs[5]: page_hidden()

if __name__ == "__main__":
    main()
