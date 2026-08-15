"""Streamlit frontend for the AI Travel Planner."""

import os
from datetime import datetime

import streamlit as st
from langchain_core.messages import HumanMessage

from main import app, storage_mode


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================================
# CUSTOM CSS
# ============================================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* =========================================================
   GLOBAL
   ========================================================= */

html,
body,
.stApp,
[data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
    background: #080d14 !important;
    color: #e8f4ff !important;
}

[data-testid="stMain"] {
    background: #080d14 !important;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1500px !important;
}


/* =========================================================
   SIDEBAR
   ========================================================= */

[data-testid="stSidebar"] {
    background: #090e18 !important;
    border-right: 1px solid #1e2e44 !important;
}

[data-testid="stSidebar"] * {
    color: #e0edf8 !important;
}

.sidebar-title {
    color: #f3f8ff !important;
    font-size: 1.05rem;
    font-weight: 700;
    margin: 0.8rem 0 0.6rem;
}

.sidebar-memory {
    color: #9db5ca !important;
    font-size: 0.78rem;
    line-height: 1.5;
    margin-bottom: 1.2rem;
}

.sidebar-chip {
    background: #0e1a2b;
    border: 1px solid #29415c;
    border-radius: 9px;
    padding: 0.65rem 0.8rem;
    margin-bottom: 0.5rem;
    color: #d5e9f8 !important;
    font-size: 0.9rem;
}

.sidebar-description {
    color: #839bb0 !important;
    font-size: 0.76rem;
    line-height: 1.5;
    margin-top: 1.2rem;
}


/* =========================================================
   HERO
   ========================================================= */

.hero {
    position: relative;
    min-height: 330px;
    border-radius: 22px;
    overflow: hidden;
    margin-bottom: 2rem;
    border: 1px solid #29415c;
    box-shadow: 0 15px 45px rgba(0, 0, 0, 0.3);

    background:
        linear-gradient(
            rgba(5, 15, 28, 0.58),
            rgba(5, 15, 28, 0.88)
        ),
        url("https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1600&q=85")
        center / cover no-repeat;

    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.hero-content {
    padding: 3rem 2rem;
    max-width: 850px;
}

.hero-badge {
    display: inline-block;
    color: #8dcbff !important;
    background: rgba(55, 130, 210, 0.18);
    border: 1px solid rgba(90, 165, 235, 0.45);
    border-radius: 30px;
    padding: 0.45rem 1rem;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.hero-title {
    color: #ffffff !important;
    font-size: 3rem;
    font-weight: 700;
    line-height: 1.15;
    margin-bottom: 1rem;
}

.hero-sub {
    color: #d4e5f4 !important;
    font-size: 1rem;
    line-height: 1.7;
    max-width: 720px;
    margin: auto;
}


/* =========================================================
   SECTION TITLES
   ========================================================= */

.section-title {
    color: #f3f8ff !important;
    font-size: 1.2rem;
    font-weight: 700;
    border-bottom: 1px solid #263d56;
    padding-bottom: 0.6rem;
    margin: 1.5rem 0 1rem;
}


/* =========================================================
   INPUT AREA
   ========================================================= */

.stTextArea textarea {
    background: #0a1520 !important;
    color: #f0f7ff !important;
    border: 1px solid #35516d !important;
    border-radius: 12px !important;
    font-size: 0.95rem !important;
}

.stTextArea textarea::placeholder {
    color: #7893aa !important;
    opacity: 1 !important;
}

.stTextArea textarea:focus {
    border-color: #4ea8f0 !important;
    box-shadow: 0 0 0 1px #4ea8f0 !important;
}


/* =========================================================
   BUTTONS
   ========================================================= */

.stButton > button {
    background: #f7f9fc !important;
    color: #162334 !important;
    border: 1px solid #cbd7e3 !important;
    border-radius: 10px !important;
    min-height: 44px !important;
    font-weight: 700 !important;
    transition: all 0.2s ease !important;
}

.stButton > button p,
.stButton > button span,
.stButton > button div {
    color: #162334 !important;
    font-weight: 700 !important;
}

.stButton > button:hover {
    background: #e8f3fb !important;
    border-color: #4ea8f0 !important;
    transform: translateY(-1px);
}

.stButton > button:disabled {
    background: #dbe4ed !important;
    color: #52677a !important;
    opacity: 1 !important;
}


/* =========================================================
   AGENT EXPANDERS
   ========================================================= */

[data-testid="stExpander"] {
    background: #0d1623 !important;
    border: 1px solid #263d56 !important;
    border-radius: 12px !important;
    margin-bottom: 0.7rem !important;
}

[data-testid="stExpander"] summary {
    background: #101d2c !important;
    border-radius: 12px !important;
}

[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] summary div {
    color: #eaf4ff !important;
    font-weight: 650 !important;
}


/* =========================================================
   OUTPUT BOX
   ========================================================= */

.output-box {
    background: #0a1520;
    border: 1px solid #22384e;
    border-radius: 10px;
    padding: 1rem;
    color: #dceeff;
    line-height: 1.65;
    margin-top: 0.5rem;
}


/* =========================================================
   FINAL PLAN
   ========================================================= */

.final-plan {
    background: #0d1724;
    border: 1px solid #2c465f;
    border-radius: 15px;
    padding: 1.5rem;
    margin-top: 0.5rem;
}

.final-plan h1,
.final-plan h2,
.final-plan h3,
.final-plan h4 {
    color: #ffffff !important;
}

.final-plan p,
.final-plan li {
    color: #dceeff !important;
    line-height: 1.7;
}

.final-plan strong {
    color: #ffffff !important;
}


/* =========================================================
   METRICS
   ========================================================= */

.metric {
    background: #0e1623;
    border: 1px solid #263d56;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}

.metric-value {
    color: #61b6ff !important;
    font-size: 1.7rem;
    font-weight: 700;
}

.metric-label {
    color: #9dbbd3 !important;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 0.25rem;
}


/* =========================================================
   DOWNLOAD
   ========================================================= */

.download-info {
    color: #8fa9bf !important;
    font-size: 0.8rem;
    margin-top: 0.6rem;
}


/* =========================================================
   STREAMLIT MARKDOWN
   ========================================================= */

.stMarkdown {
    color: #e8f4ff !important;
}

.stMarkdown p,
.stMarkdown li {
    color: #dceeff !important;
}

.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4 {
    color: #ffffff !important;
}

.stMarkdown code {
    color: #8fd0ff !important;
    background: #101d2c !important;
    border-radius: 5px !important;
}


/* =========================================================
   SPINNER
   ========================================================= */

.stSpinner > div {
    border-top-color: #4ea8f0 !important;
}


/* =========================================================
   HIDE STREAMLIT DEFAULT UI
   ========================================================= */

#MainMenu,
footer {
    visibility: hidden;
}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 900px) {
    .hero {
        min-height: 280px;
    }

    .hero-title {
        font-size: 2.2rem;
    }

    .hero-sub {
        font-size: 0.9rem;
    }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================================
# SIDEBAR
# ============================================================================

with st.sidebar:

    st.markdown(
        """<div class="sidebar-title">✈️ AI Travel Planner</div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""<div class="sidebar-memory"><b>Memory:</b><br>{storage_mode}</div>""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """<div class="sidebar-title">Powered by</div>""",
        unsafe_allow_html=True,
    )

    technologies = [
        "🔗 LangGraph",
        "🧠 Groq · LLaMA 3.3 70B",
        "🐘 PostgreSQL",
        "🔎 Tavily Search",
        "✈️ AviationStack",
    ]

    for technology in technologies:
        st.markdown(
            f"""<div class="sidebar-chip">{technology}</div>""",
            unsafe_allow_html=True,
        )

    st.markdown(
        """<div class="sidebar-title" style="margin-top:1.4rem;">Agent Pipeline</div>""",
        unsafe_allow_html=True,
    )

    pipeline_steps = [
        "① Flight Agent",
        "② Hotel Agent",
        "③ Itinerary Agent",
        "④ Final Agent",
    ]

    for step in pipeline_steps:
        st.markdown(
            f"""<div class="sidebar-chip">{step}</div>""",
            unsafe_allow_html=True,
        )

    st.markdown(
        """<div class="sidebar-description">
        PostgreSQL provides persistent LangGraph conversation
        history when the database is available.
        </div>""",
        unsafe_allow_html=True,
    )


# ============================================================================
# HERO
# ============================================================================

# IMPORTANT:
# Keep the complete HTML in one continuous string.
# This prevents Streamlit from rendering the HTML tags as visible text.

hero_html = """
<div class="hero">
    <div class="hero-content">
        <div class="hero-badge">MULTI-AGENT AI SYSTEM</div>
        <div class="hero-title">✈️ AI Travel Planner</div>
        <div class="hero-sub">
            A LangGraph-powered travel planning workflow that researches
            flights, hotels, and itinerary options before producing a
            consolidated trip plan.
        </div>
    </div>
</div>
"""

st.markdown(hero_html, unsafe_allow_html=True)


# ============================================================================
# USER INPUT
# ============================================================================

st.markdown(
    """<div class="section-title">Describe your trip</div>""",
    unsafe_allow_html=True,
)


# Quick examples
example_columns = st.columns(4)

examples = [
    "7-day Japan trip under ₹2L",
    "5-day Paris trip",
    "Dubai weekend trip",
    "10-day Bali backpacking trip",
]

if "travel_query" not in st.session_state:
    st.session_state.travel_query = ""

for column, example in zip(example_columns, examples):
    with column:
        if st.button(
            example,
            use_container_width=True,
            key=f"example_{example}",
        ):
            st.session_state.travel_query = example
            st.rerun()


user_query = st.text_area(
    "Travel request",
    value=st.session_state.travel_query,
    height=130,
    placeholder=(
        "Example: Plan a 7-day Japan trip including flights, "
        "hotels and sightseeing under ₹2 lakhs."
    ),
    label_visibility="collapsed",
)


generate = st.button(
    "🚀 Generate Travel Plan",
    use_container_width=True,
    type="primary",
)


# ============================================================================
# AGENT PIPELINE
# ============================================================================

if generate:

    if not user_query.strip():

        st.warning("Please describe your trip first.")

    else:

        st.markdown(
            """<div class="section-title">Agent Pipeline — Live</div>""",
            unsafe_allow_html=True,
        )

        collected = {
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "final_response": "",
            "llm_calls": 0,
        }

        node_labels = {
            "flight_agent": ("✈️", "Flight Agent"),
            "hotel_agent": ("🏨", "Hotel Agent"),
            "itinerary_agent": ("🗺️", "Itinerary Agent"),
            "final_agent": ("🧠", "Final Agent"),
        }

        initial_state = {
            "messages": [
                HumanMessage(content=user_query)
            ],
            "user_query": user_query,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0,
        }

        config = {
            "configurable": {
                "thread_id": "soham_user"
            }
        }

        try:

            with st.spinner("🤖 AI agents are researching your trip..."):

                for state_update in app.stream(
                    initial_state,
                    config=config,
                    stream_mode="updates",
                ):

                    for node_name, state in state_update.items():

                        if node_name not in node_labels:
                            continue

                        icon, label = node_labels[node_name]

                        with st.expander(
                            f"{icon} {label}",
                            expanded=True,
                        ):

                            # ------------------------------------------------
                            # Flight Agent
                            # ------------------------------------------------

                            if node_name == "flight_agent":

                                text = state.get(
                                    "flight_results",
                                    "",
                                )

                                collected["flight_results"] = text

                                if text:
                                    st.markdown(text)
                                else:
                                    st.info(
                                        "No flight data was returned."
                                    )

                            # ------------------------------------------------
                            # Hotel Agent
                            # ------------------------------------------------

                            elif node_name == "hotel_agent":

                                text = state.get(
                                    "hotel_results",
                                    "",
                                )

                                collected["hotel_results"] = text

                                if text:
                                    st.markdown(text)
                                else:
                                    st.info(
                                        "No hotel data was returned."
                                    )

                            # ------------------------------------------------
                            # Itinerary Agent
                            # ------------------------------------------------

                            elif node_name == "itinerary_agent":

                                text = state.get(
                                    "itinerary",
                                    "",
                                )

                                collected["itinerary"] = text

                                if text:
                                    st.markdown(text)
                                else:
                                    st.info(
                                        "No itinerary was generated."
                                    )

                            # ------------------------------------------------
                            # Final Agent
                            # ------------------------------------------------

                            elif node_name == "final_agent":

                                messages = state.get(
                                    "messages",
                                    [],
                                )

                                if messages:
                                    text = messages[-1].content
                                else:
                                    text = ""

                                collected["final_response"] = text

                                if text:
                                    st.markdown(text)
                                else:
                                    st.info(
                                        "No final response was generated."
                                    )

                        collected["llm_calls"] = state.get(
                            "llm_calls",
                            collected["llm_calls"],
                        )


            # =================================================================
            # EXECUTION SUMMARY
            # =================================================================

            st.markdown(
                """<div class="section-title">Execution Summary</div>""",
                unsafe_allow_html=True,
            )

            metric1, metric2, metric3 = st.columns(3)

            with metric1:
                st.markdown(
                    """<div class="metric">
                    <div class="metric-value">4</div>
                    <div class="metric-label">Agents Run</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

            with metric2:
                st.markdown(
                    f"""<div class="metric">
                    <div class="metric-value">{collected["llm_calls"]}</div>
                    <div class="metric-label">LLM Calls</div>
                    </div>""",
                    unsafe_allow_html=True,
                )

            with metric3:
                st.markdown(
                    """<div class="metric">
                    <div class="metric-value">✓</div>
                    <div class="metric-label">Completed</div>
                    </div>""",
                    unsafe_allow_html=True,
                )


            # =================================================================
            # FINAL TRAVEL PLAN
            # =================================================================

            st.markdown(
                """<div class="section-title">🧠 Final Travel Plan</div>""",
                unsafe_allow_html=True,
            )

            final_text = collected["final_response"]

            if not final_text:
                final_text = collected["itinerary"]

            if not final_text:
                final_text = "No travel plan was generated."

            st.markdown(
                '<div class="final-plan">',
                unsafe_allow_html=True,
            )

            st.markdown(final_text)

            st.markdown(
                '</div>',
                unsafe_allow_html=True,
            )


            # =================================================================
            # SAVE / DOWNLOAD
            # =================================================================

            timestamp = datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )

            markdown_plan = f"""# AI Travel Plan

**Query:** {user_query}

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**User ID:** soham_user

---

## ✈️ Flight Information

{collected["flight_results"] or "N/A"}

---

## 🏨 Hotel Information

{collected["hotel_results"] or "N/A"}

---

## 🗺️ Itinerary

{collected["itinerary"] or "N/A"}

---

## 🧠 Final Travel Plan

{collected["final_response"] or "N/A"}

---

**LLM Calls:** {collected["llm_calls"]}
"""

            save_dir = os.path.join(
                os.path.dirname(__file__),
                "travel_plans",
            )

            os.makedirs(
                save_dir,
                exist_ok=True,
            )

            filename = (
                f"travel_plan_{timestamp}.md"
            )

            filepath = os.path.join(
                save_dir,
                filename,
            )

            with open(
                filepath,
                "w",
                encoding="utf-8",
            ) as file:
                file.write(markdown_plan)

            st.download_button(
                "⬇️ Download Travel Plan",
                data=markdown_plan,
                file_name=filename,
                mime="text/markdown",
                use_container_width=True,
            )

            st.markdown(
                f"""<div class="download-info">
                ✓ Plan automatically saved to:
                <b>travel_plans/{filename}</b>
                </div>""",
                unsafe_allow_html=True,
            )

        except Exception as exc:

            st.error(
                "The travel planning workflow encountered an error."
            )

            st.exception(exc)