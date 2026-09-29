"""Home Management Compass: two-property preventive care and administration."""
from datetime import datetime
from zoneinfo import ZoneInfo
import streamlit as st
from content import LESSONS,SOURCES
from visuals import show
from tracker import render as task_log

st.set_page_config(page_title="Home Management Compass",page_icon="🏠",layout="wide")
st.title("🏠 Home Management Compass")
st.caption("Santa Clara owner-occupied home + Sunnyvale rented townhome · General guidance reviewed 29 September 2026")
st.info("Safety first: leave a dangerous area and contact emergency/utility services for suspected gas, fire, carbon monoxide or serious electrical hazards. California and Sunnyvale rules, lease terms, HOA documents, manufacturer instructions and permits govern specific work; verify them for each property.")
PROPERTY=st.selectbox("Which property are you planning for?",["Santa Clara single-family home","Sunnyvale rented townhome"])
IS_RENTAL=PROPERTY.startswith("Sunnyvale")
TODAY=datetime.now(ZoneInfo("America/Los_Angeles")).date()
NAMES=["📌 Master dashboard","🏠 Property overview"]+[f"{x['icon']} {x['title']}" for x in LESSONS]+["📅 Task log","🧰 Repair & cost tools","🏘️ Rental administration","📚 Sources"]
tabs=st.tabs(NAMES)

with tabs[0]:
    st.header("📌 Two-property master dashboard")
    st.caption("Selected property: "+PROPERTY+" · Planning date: "+TODAY.isoformat())
    a,b,c=st.columns(3)
    a.metric("System lessons",len(LESSONS));b.metric("Properties",2);c.metric("Priority","Safety → water → continuity")
    st.dataframe([{"System":x["title"],"Priority":"High" if x["title"].startswith(("Safety","Water","Electrical","Rental","Emergency")) else "Review","Why it matters":x["takeaway"],"First action":x["action"],"Santa Clara focus":"Owner controls home systems" if x["title"]!="Rental townhome and tenant coordination" else "Not applicable","Sunnyvale focus":"Check tenant, lease and HOA responsibility" if x["title"]!="Rental townhome and tenant coordination" else "Acknowledge and track tenant reports","Original source":SOURCES[x["sources"][0]]} for x in LESSONS],hide_index=True,use_container_width=True,height=565,column_config={"Original source":st.column_config.LinkColumn("Original source")})
    st.subheader("🚦 Issue triage quick reference")
    st.dataframe([
        {"Urgency":"Immediate danger","Examples":"Gas smell, fire, CO alarm, arcing","First response":"Leave area; use emergency/utility services; do not DIY","Document":"Time, incident and professional response"},
        {"Urgency":"Active damage / essential service","Examples":"Water escaping, sewage, no essential heat","First response":"Contain only if safe; contact qualified service; for rental coordinate promptly","Document":"Photos, tenant report and work order"},
        {"Urgency":"Planned maintenance","Examples":"Dirty HVAC filter, leaf buildup, warranty review","First response":"Schedule and verify responsibility","Document":"Date, invoice and next review"},
    ],hide_index=True,use_container_width=True)
    st.subheader("🚫 Common mistakes and better alternatives")
    st.dataframe([
        {"Mistake":"No shutoff map","Why":"Only look during a leak","Better step":"Label accessible valves before an incident","Helpful tool":"Property emergency card"},
        {"Mistake":"Ignoring a wet spot","Why":"Seems cosmetic","Better step":"Find moisture source promptly","Helpful tool":"Dated photos and qualified inspection"},
        {"Mistake":"Guessing contractor quality from price","Why":"Bids have different scopes","Better step":"Compare written identical scopes; check CSLB","Helpful tool":"Bid comparison table"},
        {"Mistake":"Forgetting equipment details","Why":"Manuals and invoices scattered","Better step":"Record model, age, repair history","Helpful tool":"Asset inventory"},
        {"Mistake":"Unclear tenant/HOA responsibility","Why":"Shared systems and lease terms differ","Better step":"Check documents, record communication and current rules","Helpful tool":"Rental issue log"},
    ],hide_index=True,use_container_width=True)
    st.markdown(f"**Current authority links:** [Santa Clara permits ↗]({SOURCES['Santa Clara permits']}) · [Sunnyvale permits ↗]({SOURCES['Sunnyvale permits']}) · [California rental repairs ↗]({SOURCES['California repairs']})")

with tabs[1]:
    st.header("🏠 Two homes, separate records")
    st.write("For the Santa Clara home, focus on owner-controlled systems, roof and gutters, garage-door safety, appliance records and emergency readiness. For the Sunnyvale rental, add tenant reports, entry coordination, lease/HOA allocation, habitability and insurance. Confirm actual features before using any task template.")
    st.dataframe([{"Property":"Santa Clara single-family home","Management focus":"Owner maintenance, systems, gutters and garage access","First check":"Shutoffs, smoke alarms, model numbers"},{"Property":"Sunnyvale rented townhome","Management focus":"Repairs, tenant communication, lease/HOA, local protections","First check":"Open issues, emergency contact route, governing documents"}],hide_index=True,use_container_width=True)
    st.markdown("**First action:** select a property above, then open its Task log and export a separate CSV.")
    show("Property overview",["Select home","Map assets","Assign owner","Track work"])

for tab,lesson in zip(tabs[2:2+len(LESSONS)],LESSONS):
    with tab:
        st.header(f"{lesson['icon']} {lesson['title']}")
        st.caption(lesson["level"]+" · "+lesson["takeaway"])
        st.dataframe([{"Concept":n,"What it means":meaning,"Example":example} for n,meaning,example in lesson["concepts"]],hide_index=True,use_container_width=True)
        st.markdown("**Example:** "+lesson["example"])
        st.markdown("**Next step:** "+lesson["action"])
        if IS_RENTAL:st.info("For the Sunnyvale rental: confirm lease/HOA responsibility, coordinate entry as required, document tenant communications, and check current city and California guidance.")
        else:st.info("For the Santa Clara home: identify the actual equipment and check city permits before regulated repairs; use qualified help for hazardous work.")
        with st.expander("🧠 Knowledge check: "+lesson["question"]):
            st.text_area("Your answer",key="draft_"+lesson["title"],height=70)
            if st.checkbox("Reveal practical answer",key="reveal_"+lesson["title"]):st.success(lesson["answer"])
        st.subheader("🔎 Original guidance")
        cols=st.columns(len(lesson["sources"]))
        for col,name in zip(cols,lesson["sources"]):
            with col:st.markdown(f"**{name}**  \n[Open source ↗]({SOURCES[name]})")
        show(lesson["title"],lesson["visual"])

with tabs[-4]:
    st.header("📅 Maintain a task log for "+PROPERTY)
    task_log(PROPERTY)
    st.markdown(f"[ENERGY STAR HVAC guidance ↗]({SOURCES['ENERGY STAR HVAC']}) · [USFA smoke alarm guidance ↗]({SOURCES['USFA smoke alarms']})")
    show("Task log",["Choose home","Edit tasks","Export CSV","Follow up"])

with tabs[-3]:
    st.header("🧰 Repair triage and cost tools")
    mode=st.selectbox("Choose a tool",["Repair triage","Compare contractor bids","Monthly reserve planner"])
    if mode=="Repair triage":
        issue=st.selectbox("Issue type",["Gas/fire/CO or sparking","Active water leak or sewage","Essential service failure","Garage door spring/cable concern","Cosmetic or planned maintenance"])
        guidance={
            "Gas/fire/CO or sparking":"Leave the danger area; use emergency/utility services. Do not attempt a repair.",
            "Active water leak or sewage":"Contain or shut off water only if safe; document and arrange qualified help promptly. For the rental, coordinate with the tenant.",
            "Essential service failure":"Assess habitability and safety promptly; arrange qualified service and check rental obligations if applicable.",
            "Garage door spring/cable concern":"Stop operating the door and use a qualified garage-door professional; avoid spring or cable work.",
            "Cosmetic or planned maintenance":"Document the scope, check permits/HOA, verify contractor and compare written bids.",
        }
        st.warning(guidance[issue])
    elif mode=="Compare contractor bids":
        st.caption("Enter estimates for the same written scope. Price alone is not a recommendation.")
        rows=[]
        for i in range(1,4):
            a,b=st.columns(2)
            cost=a.number_input(f"Bid {i} total ($)",min_value=0.0,value=0.0,step=100.0,key=f"bid_{i}")
            warranty=b.number_input(f"Bid {i} warranty months (if stated)",min_value=0,value=0,step=1,key=f"warranty_{i}")
            rows.append({"Bid":i,"Quoted total ($)":cost,"Warranty months stated":warranty,"License, scope, permits and insurance":"Verify separately"})
        st.dataframe(rows,hide_index=True,use_container_width=True)
        st.markdown(f"[Verify California license ↗]({SOURCES['CSLB license check']}) · [CSLB bid checklist ↗]({SOURCES['CSLB hiring']})")
    else:
        annual=st.number_input("Planned yearly maintenance ($)",min_value=0.0,value=1200.0,step=100.0)
        project=st.number_input("Known upcoming repair/replacement ($)",min_value=0.0,value=2400.0,step=100.0)
        months=st.slider("Months until planned project",1,60,24)
        buffer=st.number_input("Existing dedicated reserve ($)",min_value=0.0,value=0.0,step=100.0)
        target=annual/12+max(0,project-buffer)/months
        st.metric("Illustrative monthly set-aside",f"${target:,.0f}")
        st.caption("Arithmetic planning estimate only; it omits unknown emergencies, inflation, insurance coverage and tax treatment. Keep property budgets separate.")
    show("Repair tools",["Describe","Triage","Verify","Document"])

with tabs[-2]:
    st.header("🏘️ Rental townhome administration")
    st.write("Use this tab for the Sunnyvale rental even when the Santa Clara property is selected. It is a checklist for records and communication, not a legal deadline calculator.")
    st.dataframe([
        {"Area":"Repair intake","What to keep":"Date reported, description, photos, urgency, response, completion","Check":"Habitability and prompt follow-through","Authority":SOURCES["California repairs"]},
        {"Area":"Entry and scheduling","What to keep":"Notice and agreed access details","Check":"Current law, lease and exception conditions","Authority":SOURCES["California tenant guide"]},
        {"Area":"HOA and exterior","What to keep":"Governing documents, approval and maintenance allocation","Check":"Confirm who controls and pays for shared systems","Authority":SOURCES["Sunnyvale permits"]},
        {"Area":"Tenant protections","What to keep":"Required notices and lease documents","Check":"Review current Sunnyvale and state rules","Authority":SOURCES["Sunnyvale tenant protections"]},
        {"Area":"Deposit and move-out","What to keep":"Move-in condition, permitted deductions, dated itemization","Check":"Current California rules; no unsupported deduction","Authority":SOURCES["California DOJ tenants"]},
        {"Area":"Insurance and costs","What to keep":"Landlord policy, HOA master policy, invoices","Check":"Coverage gaps and deductibles","Authority":SOURCES["NAIC home insurance"]},
    ],hide_index=True,use_container_width=True,column_config={"Authority":st.column_config.LinkColumn("Authority")})
    st.caption("Property-specific facts and legal requirements may change. Do not enter tenant names or private access details in a shared export.")
    show("Rental administration",["Receive report","Triage","Coordinate","Close out"])

with tabs[-1]:
    st.header("📚 Sources and method")
    st.write("Direct government and public-interest sources support the safety and maintenance lessons. Suggested review dates outside official alarm/filter guidance are planning prompts. Verify actual product manuals, city permits, HOA documents, insurance terms and current California law.")
    st.dataframe([{"Source":name,"Direct link":url} for name,url in SOURCES.items()],hide_index=True,use_container_width=True,column_config={"Direct link":st.column_config.LinkColumn("Direct link")})
    st.caption("The app does not contact vendors, tenants or third parties. Edited task rows remain in the Streamlit session until you export them; the code has no database or scheduled reminders.")
    show("Sources",["Identify claim","Open source","Check scope","Act safely"])
