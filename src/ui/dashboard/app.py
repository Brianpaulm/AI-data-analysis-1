import streamlit as st
import pandas as pd
import chardet
import pdfplumber
from core.analytics.descriptive import describe
from core.analytics.quality import data_quality_score
from core.logging.logger import AuditLogger
import re

# Initialize audit logger
logger = AuditLogger("dashboard")

st.set_page_config(page_title="Secure Data Dashboard", layout="wide")
st.title("Secure Data Analysis Dashboard")

uploaded = st.file_uploader("Upload a data file", type=None)

def parse_transcript_pdf(pdf_file):
    """Parse transcript PDF into structured DataFrame"""
    rows = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            lines = text.split("\n")
            for line in lines:
                # Detect unit lines using regex (e.g., starts with BLW)
                match = re.match(r"(BLW\d{4})\s+(.+?)\s+(\d+)\s+(\d+)\s+([A-F]|CT|Exempt)", line)
                if match:
                    unit_code, unit_title, hours, marks, grade = match.groups()
                    rows.append([unit_code, unit_title, int(hours), int(marks), grade])
    df = pd.DataFrame(rows, columns=["UnitCode", "UnitTitle", "Hours", "Marks", "Grade"])
    return df

if uploaded:
    try:
        filename = uploaded.name.lower()

        # PDF handling
        if filename.endswith(".pdf"):
            try:
                df = parse_transcript_pdf(uploaded)

                if df.empty:
                    st.warning("No structured table detected in PDF. Showing text preview.")
                    with pdfplumber.open(uploaded) as pdf:
                        all_text = "".join([page.extract_text() + "\n" for page in pdf.pages])
                    st.text(all_text[:2000])
                    logger.log("pdf_no_table", {"filename": uploaded.name})
                else:
                    st.subheader("Parsed PDF Table Preview")
                    st.dataframe(df.head(50))

                    st.subheader("Descriptive Statistics")
                    st.dataframe(describe(df.select_dtypes(include='number')))

                    st.subheader("Data Quality Score")
                    st.metric("Quality", data_quality_score(df))

                    logger.log("pdf_parsed_success", {"filename": uploaded.name, "rows": len(df)})

            except Exception as e:
                st.error(f"Failed to read PDF: {e}")
                logger.log("pdf_read_failure", {"filename": uploaded.name, "error": str(e)})

        # CSV/TSV/Text handling
        else:
            raw_data = uploaded.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding'] if result['encoding'] else None
            uploaded.seek(0)

            fallback_encodings = ["utf-8", "ISO-8859-1", "windows-1252", "latin1"]
            df = None
            last_error = None
            for enc in ([encoding] + fallback_encodings if encoding else fallback_encodings):
                try:
                    uploaded.seek(0)
                    df = pd.read_csv(uploaded, engine="python", on_bad_lines="skip", encoding=enc)
                    logger.log("file_read_success", {"filename": uploaded.name, "encoding": enc})
                    break
                except Exception as e:
                    last_error = e
                    continue

            if df is None:
                raise last_error

            st.subheader("Preview")
            st.dataframe(df.head(50))

            st.subheader("Descriptive Statistics")
            st.dataframe(describe(df.select_dtypes(include='number')))

            st.subheader("Data Quality Score")
            st.metric("Quality", data_quality_score(df))

    except Exception as e:
        st.error(f"Failed to read file: {e}")
        logger.log("file_read_failure", {"filename": uploaded.name, "error": str(e)})
