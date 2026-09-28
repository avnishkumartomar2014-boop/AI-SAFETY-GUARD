import streamlit as st
import requests


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = "http://127.0.0.1:8000/analyze"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(

    page_title="AI Safety Guard",

    page_icon="🛡️",

    layout="wide"
)


# ============================================================
# HEADER
# ============================================================

st.title(
    "🛡️ AI Safety Guard"
)

st.subheader(
    "Real-Time LLM Safety & Hallucination Detection"
)

st.write(
    "This prototype detects jailbreak attempts, "
    "blocks malicious prompts, and evaluates "
    "response grounding."
)

st.divider()


# ============================================================
# USER INPUT
# ============================================================

st.subheader(
    "🔍 Enter User Prompt"
)

prompt = st.text_area(

    "Prompt",

    placeholder=
    "Example: What does the free plan provide?",

    height=120
)


# ============================================================
# ANALYZE BUTTON
# ============================================================

if st.button(
    "🚀 Analyze Prompt",
    type="primary"
):

    if not prompt.strip():

        st.warning(
            "Please enter a prompt."
        )

    else:

        try:

            with st.spinner(
                "Running safety checks..."
            ):

                response = requests.post(

                    API_URL,

                    json={
                        "prompt": prompt
                    },

                    timeout=10
                )


            data = response.json()


            st.divider()


            # =================================================
            # BLOCKED PROMPT
            # =================================================

            if data["status"] == "BLOCKED":

                st.error(
                    "🚨 PROMPT BLOCKED"
                )

                st.write(
                    data["message"]
                )


                jailbreak = data[
                    "jailbreak"
                ]


                col1, col2, col3 = st.columns(3)


                with col1:

                    st.metric(
                        "Risk Level",
                        jailbreak["risk"]
                    )


                with col2:

                    st.metric(
                        "Jailbreak Score",
                        jailbreak["score"]
                    )


                with col3:

                    st.metric(
                        "Latency",
                        f'{data["latency_ms"]} ms'
                    )


                st.subheader(
                    "🚨 Detected Attack Patterns"
                )


                for pattern in jailbreak[
                    "detected_patterns"
                ]:

                    st.write(
                        f"• {pattern}"
                    )


            # =================================================
            # ALLOWED PROMPT
            # =================================================

            else:

                st.success(
                    "✅ PROMPT ALLOWED"
                )


                jailbreak = data[
                    "jailbreak"
                ]


                # ---------------------------------------------
                # SECURITY
                # ---------------------------------------------

                st.subheader(
                    "🔐 Security Analysis"
                )


                col1, col2, col3 = st.columns(3)


                with col1:

                    st.metric(
                        "Jailbreak Risk",
                        jailbreak["risk"]
                    )


                with col2:

                    st.metric(
                        "Jailbreak Score",
                        jailbreak["score"]
                    )


                with col3:

                    st.metric(
                        "Guardrail Latency",
                        f'{data["latency_ms"]} ms'
                    )


                # ---------------------------------------------
                # AI RESPONSE
                # ---------------------------------------------

                st.subheader(
                    "🤖 AI Response"
                )


                st.info(
                    data["answer"]
                )


                # ---------------------------------------------
                # HALLUCINATION
                # ---------------------------------------------

                st.subheader(
                    "📚 Hallucination Analysis"
                )


                col1, col2, col3 = st.columns(3)


                with col1:

                    st.metric(
                        "Grounding Score",
                        f'{data["grounding_score"]}%'
                    )


                with col2:

                    st.metric(
                        "Hallucination Risk",
                        f'{data["hallucination_risk"]}%'
                    )


                with col3:

                    st.metric(
                        "Factual Status",
                        data["factual_status"]
                    )


                st.write(
                    "Knowledge Base Grounding"
                )


                st.progress(
                    min(
                        data["grounding_score"] / 100,
                        1.0
                    )
                )


        except Exception as error:

            st.error(
                f"Could not connect to Safety Engine: {error}"
            )
