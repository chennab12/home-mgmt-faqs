# Home Management Compass

A separate Streamlit dashboard for two properties: an owner-occupied single-family home in Santa Clara and a rented townhome in Sunnyvale. Seventeen lessons progress from inventory and safety to plumbing, HVAC, roof and gutters, electrical work, appliances, garage doors, moisture, vendor selection, permits, insurance, bills and tax records, tenant coordination, costs and emergencies. Each lesson includes a concept table, example, quiz, original-source links and animated memory cue. The first tab is a consolidated dashboard.

The Task log offers editable sample tasks per property, CSV export and CSV restoration. Sample dates are planning prompts, not legal deadlines. Exports should be stored privately; do not enter tenant names, access codes, addresses or account numbers. Changes are session-only unless exported and restored; there is no database, notification service, vendor contact or tenant messaging. The tools include repair triage, side-by-side bid inputs and a transparent monthly reserve estimate.

State and city rules, permit requirements, lease/HOA allocations and insurance terms vary and may change. The app links to California DRE/DOJ, Sunnyvale, Santa Clara, CSLB, ENERGY STAR, EPA, USFA/FEMA and NAIC. Safety emergencies require appropriate emergency services and qualified professionals.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

For Streamlit Community Cloud, deploy this directory with `app.py` as the entry point. No API key is required.
