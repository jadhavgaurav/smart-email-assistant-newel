import streamlit as st
import pandas as pd
import os
from datetime import datetime
from orchestrator import Orchestrator
import boto3
from botocore.exceptions import NoCredentialsError

# AWS config
AWS_BUCKET_NAME = "your-s3-bucket-name"
AWS_REGION = "your-region"
AWS_LOG_KEY = "smart-email-assistant/history.csv"

# App + log setup
st.set_page_config(page_title="Smart Email Assistant", page_icon="📬", layout="wide")
orchestrator = Orchestrator()
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "history.csv")
os.makedirs(LOG_DIR, exist_ok=True)

tabs = st.tabs(["📨 Assistant", "📂 View History"])

# --- TAB 1: ASSISTANT ---
with tabs[0]:
    st.markdown("<h1 style='text-align: center;'>📬 Smart Email Assistant</h1>", unsafe_allow_html=True)
    email_text = st.text_area("✉️ Enter email content below:", height=200)
    submit = st.button("Generate Reply")

    if submit and email_text.strip():
        with st.spinner("🔍 Processing..."):
            result = orchestrator.handle_email(email_text)

        st.markdown("---")
        st.markdown("### 🧠 Classification Result")
        st.write(f"**Category**: {result['predicted_category']}")
        st.write(f"**Confidence**: {result['confidence']:.2f}")

        st.markdown("### 🤖 System Action")
        st.write(f"**Action**: {result['action']}")

        if result['action'] == "Responded":
            st.markdown("### ✉️ Suggested Response")
            st.success(result["response"])
        else:
            st.markdown("### 🚨 Escalation Triggered")
            st.warning(result["escalation_message"])

        # Logging
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "email_text": email_text,
            "category": result["predicted_category"],
            "confidence": result["confidence"],
            "action": result["action"],
            "response": result.get("response", ""),
            "escalation_message": result.get("escalation_message", "")
        }

        df = pd.DataFrame([log_entry])
        df.to_csv(LOG_FILE, mode="a", header=not os.path.exists(LOG_FILE), index=False)
        st.success("✅ Interaction saved to history log!")

    elif submit:
        st.warning("Please enter some email content to process.")

# --- TAB 2: VIEW HISTORY ---
with tabs[1]:
    st.markdown("<h2>📂 Logged Email History</h2>", unsafe_allow_html=True)

    if os.path.exists(LOG_FILE):
        history_df = pd.read_csv(LOG_FILE)
        st.dataframe(history_df, use_container_width=True)

        # Download CSV
        csv = history_df.to_csv(index=False).encode("utf-8")
        st.download_button("📤 Download CSV Log", data=csv, file_name="history.csv", mime="text/csv")

        # Upload to S3
        if st.button("☁️ Upload to S3"):
            try:
                s3 = boto3.client("s3", region_name=AWS_REGION)
                s3.upload_file(LOG_FILE, AWS_BUCKET_NAME, AWS_LOG_KEY)
                st.success(f"✅ Uploaded to s3://{AWS_BUCKET_NAME}/{AWS_LOG_KEY}")
            except NoCredentialsError:
                st.error("❌ AWS credentials not found. Set them via environment or ~/.aws/credentials.")
            except Exception as e:
                st.error(f"❌ Upload failed: {str(e)}")
    else:
        st.info("No history log found.")
# --- END OF APP ---