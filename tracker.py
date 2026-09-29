"""Session-only editable task log with portable CSV round-trip."""
import csv
import io
from datetime import date,timedelta
import streamlit as st

FIELDS=["Property","System","Task / issue","Priority","Status","Due / review date","Owner / contact","Estimated cost ($)","Actual cost ($)","Notes"]

def default_rows(property_name):
    today=date.today()
    def row(system,task,priority,days,owner="Owner",notes="Planning reminder; check equipment manual or agreement"):
        return dict(zip(FIELDS,[property_name,system,task,priority,"Planned",(today+timedelta(days=days)).isoformat(),owner,"","",notes]))
    common=[
        row("Fire safety","Test smoke alarms and check replacement dates","High",30,notes="USFA: test monthly; follow alarm instructions"),
        row("HVAC","Inspect filter; change if dirty","Medium",30,notes="ENERGY STAR: check monthly; follow equipment guidance"),
        row("Water","Locate shutoffs and scan accessible areas for leaks","High",30),
        row("Insurance","Review coverage, deductible and renewal","Medium",90),
        row("Records","Update appliance model, warranties and service contacts","Low",60),
        row("Exterior","Observe drainage and roof/gutter symptoms from safe access","Medium",90),
    ]
    if property_name.startswith("Santa Clara"):
        common += [row("Garage door","Log opener model/error and arrange qualified inspection if needed","Medium",30),row("Gutters","Plan safe leaf-season inspection/cleaning","Medium",60)]
    else:
        common += [row("Tenant","Review open repair reports and communication log","High",14),row("HOA","Check governing documents for maintenance responsibility","Medium",45),row("Lease","Review tenant notices and current city/state guidance","Medium",60)]
    return common

def parse_csv(uploaded,property_name):
    raw=uploaded.getvalue()
    if len(raw)>500_000:raise ValueError("CSV is too large (500 KB maximum).")
    reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    if reader.fieldnames!=FIELDS:raise ValueError("CSV columns do not match this app's exported task template.")
    rows=[]
    for r in reader:
        if len(rows)>=250:raise ValueError("CSV can contain at most 250 tasks.")
        if r["Property"]!=property_name:raise ValueError("A row belongs to a different property. Select its property before importing.")
        rows.append({name:(r[name] or "")[:500] for name in FIELDS})
    return rows

def to_csv(rows):
    out=io.StringIO();writer=csv.DictWriter(out,fieldnames=FIELDS,extrasaction="ignore")
    writer.writeheader()
    for row in rows:
        # Stop spreadsheet programs from interpreting an edited cell as a formula.
        safe={k:("'"+str(row.get(k,"")) if str(row.get(k,"")).lstrip().startswith(("=","+","-","@")) else str(row.get(k,""))) for k in FIELDS}
        writer.writerow(safe)
    return out.getvalue().encode("utf-8-sig")

def render(property_name):
    st.subheader("📅 Editable property task log")
    st.caption("Sample reminders are planning prompts, not legal deadlines. Verify each date with manuals, lease, HOA and local rules. Changes remain in the Streamlit session; download CSV to keep them.")
    imported=st.file_uploader("Restore a previously exported CSV for this property",type=["csv"],key="upload_"+property_name)
    try:rows=parse_csv(imported,property_name) if imported else default_rows(property_name)
    except (ValueError,UnicodeError) as exc:
        st.error(str(exc));rows=default_rows(property_name)
    edited=st.data_editor(rows,hide_index=True,use_container_width=True,num_rows="dynamic",key="grid_"+property_name)
    if hasattr(edited,"to_dict"):edited=edited.to_dict("records")
    st.download_button("⬇️ Save this property's edited task log",to_csv(edited),file_name=("santa_clara_home_tasks.csv" if property_name.startswith("Santa Clara") else "sunnyvale_rental_tasks.csv"),mime="text/csv",key="download_"+property_name)
    st.caption("Use estimated costs only. Avoid tenant names, access codes, addresses and account details in a file you may share.")
