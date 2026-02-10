# Secure Data Analysis Dashboard

## Overview
This project is a military-grade, zero-trust, fault-tolerant data ingestion and analytics platform.
It securely ingests data from virtually any document format, normalizes it into a unified model,
performs advanced analytics, and exposes results through an analyst-grade interactive dashboard.

## Key Features
- MIME-based file intelligence
- Secure sandboxed ingestion
- Schema inference & data profiling
- Advanced analytics & automatic insights
- Streamlit-based interactive dashboard
- Full audit logging & RBAC-ready security layer

## Security Model
- Zero-trust file handling
- Hash-based integrity verification
- Encrypted temporary storage
- Pluggable malware scanning hooks
- No hardcoded secrets

## Running
```bash
export DASHBOARD_SECRET_KEY=change_me
streamlit run src/ui/dashboard/app.py
