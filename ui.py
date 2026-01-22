# import streamlit as st
# import time
# from app import run_orchestrator

# st.set_page_config(
#     page_title="AI Orchestrator",
#     page_icon="🚀",
#     layout="wide"
# )

# st.title("🤖 Multi-Agent AI Orchestrator")
# st.markdown("---")

# user_input = st.text_area(
#     "Enter your topic or question:",
#     placeholder="e.g. Current state of Quantum Computing",
#     height=120
# )

# # Rate-limit protection
# if "last_run" not in st.session_state:
#     st.session_state.last_run = 0

# if st.button("Generate Report", type="primary"):
#     if not user_input.strip():
#         st.warning("Please enter a topic.")
#     elif time.time() - st.session_state.last_run < 30:
#         st.warning("Rate limit: Please wait a few seconds before running again.")
#     else:
#         st.session_state.last_run = time.time()

#         with st.spinner(
#             "Agents are collaborating (Researching → Summarizing → Writing)..."
#         ):
#             try:
#                 # 🔧 FORCE STREAMLIT UI REFRESH
#                 st.empty()

#                 results = run_orchestrator(user_input)

#                 st.empty()

#                 # 🔍 DISPLAY OUTPUTS
#                 col1, col2 = st.columns(2)

#                 with col1:
#                     st.subheader("🔍 Detailed Research")
#                     st.write(results["research"])

#                 with col2:
#                     st.subheader("📝 Summary")
#                     st.write(results["summary"])

#                 st.markdown("---")
#                 st.subheader("📧 Professional Email Draft")
#                 st.code(results["email"], language="markdown")

#             except Exception as e:
#                 st.error(f"An error occurred: {e}")


import streamlit as st
import time
from app import run_orchestrator

st.set_page_config(
    page_title="AI Orchestrator",
    page_icon="🚀",
    layout="wide"
)

st.title("🤖 Multi-Agent AI Orchestrator")
st.markdown("---")

user_input = st.text_area(
    "Enter your topic or question:",
    placeholder="e.g. Current state of Quantum Computing",
    height=120
)

# Rate limit control
if "last_run" not in st.session_state:
    st.session_state.last_run = 0

if st.button("Generate Report", type="primary"):
    if not user_input.strip():
        st.warning("Please enter a topic.")
    elif time.time() - st.session_state.last_run < 30:
        st.warning("Rate limit: Please wait a few seconds before running again.")
    else:
        st.session_state.last_run = time.time()

        with st.spinner(
            "Agents are collaborating (Researching → Summarizing → Writing)..."
        ):
            try:
                st.empty()  # force UI refresh
                results = run_orchestrator(user_input)
                st.empty()

                # 🔍 RESEARCH (FIRST)
                st.subheader("🔍 Detailed Research")
                st.write(results["research"])

                st.markdown("---")

                # 📝 SUMMARY (SECOND)
                st.subheader("📝 Summary")
                st.write(results["summary"])

                st.markdown("---")

                # 📧 EMAIL (THIRD)
                st.subheader("📧 Professional Email Draft")
                st.text_area(
                    "Email Content",
                    results["email"],
                    height=300
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")
