import streamlit as st
from datetime import datetime, timedelta
import re

# --- Page Configuration ---
st.set_page_config(page_title="Transport Stats", layout="wide")

st.title("Transport Stats (Compact Version with Converter)")

# --- Formatting Helper ---
def fmt(number):
    """Format with commas."""
    if isinstance(number, int) or number.is_integer():
        return f"{number:,.0f}"
    return f"{number:,.2f}"

# ================= ROW 1: DATE & DAY =================
st.header("Date Selection")
yesterday = datetime.now() - timedelta(days=1)

col_date, col_day = st.columns([1, 3])
with col_date:
    selected_date = st.date_input("Date", value=yesterday)
with col_day:
    day_str = selected_date.strftime("%A")
    st.write("") # Spacing
    st.write(f"**Day:** {day_str}")

date_val = selected_date.strftime("%Y-%m-%d")

# ================= ROW 2: DATA INPUTS (3 COLUMNS) =================
st.header("Data Inputs")
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Daily Boarding")
    ev_daily_count = st.number_input("Daily Count", min_value=0, value=0, step=1)
    ev_daily_amount = st.number_input("Daily Amount", min_value=0.0, value=0.0, step=0.01)

    st.subheader("Daily Bus Count")
    total_bus = st.number_input("Total Bus", min_value=0, value=180, step=1)
    working_bus = st.number_input("Working Buses", min_value=0, value=0, step=1)

    st.subheader("MST Card Charge")
    mst_count = st.number_input("Charge Count", min_value=0, value=0, step=1)
    mst_amount = st.number_input("Charge Amount", min_value=0.0, value=0.0, step=0.01)
    mst_balance = st.number_input("Balance Amount", min_value=0.0, value=0.0, step=0.01)

with col2:
    st.subheader("Daily Card Charge")
    card_chg_count = st.number_input("Charge Count (Card)", min_value=0, value=0, step=1)
    card_chg_amount = st.number_input("Charge Amount (Card)", min_value=0.0, value=0.0, step=0.01)

    st.subheader("Daily Ticket Sales")
    ticket_sale_count = st.number_input("Ticket Sale Count", min_value=0, value=0, step=1)
    ticket_sale_amount = st.number_input("Ticket Sale Amount", min_value=0.0, value=0.0, step=0.01)

    st.subheader("QR Mobile")
    qr_count = st.number_input("Total QR Tickets", min_value=0, value=0, step=1)

with col3:
    st.subheader("Orange Line Metro")
    olm_riders = st.number_input("Total Riders", min_value=0, value=0, step=1)
    olm_revenue = st.number_input("Total Revenue", min_value=0.0, value=0.0, step=0.01)
    olm_sales = st.number_input("Total Sales", min_value=0.0, value=0.0, step=0.01)

st.divider()

# ================= CALCULATIONS =================
qr_amount = qr_count * 50
grand_total_riders = olm_riders + qr_count + ticket_sale_count
grand_total_sales = olm_sales + qr_amount + ticket_sale_amount
feeder_routes_riders = qr_count + ticket_sale_count

# ================= REPORTS =================
st.header("Generated Reports")
st.info("Hover over the top right corner of the text boxes below and click the 'Copy' icon to copy the reports to your clipboard.")

tab1, tab2 = st.tabs(["Main Template", "Short Summary"])

with tab1:
    main_template = f"""*General Statistics - EV & HEV Buses*
Date: {date_val}
Day: {day_str}
*Daily Boarding*
Daily Count: {fmt(ev_daily_count)}
Daily Amount: {fmt(ev_daily_amount)}
*Daily Bus Count*
Total Bus: {fmt(total_bus)}
Working Buses: {fmt(working_bus)}
*Daily MST Card Charge Info*
MST Card Charge Count: {fmt(mst_count)}
MST Card Charge Amount: {fmt(mst_amount)}
MST Card Balance Amount: {fmt(mst_balance)}
*Daily Card Charge*
Daily Card Charge Count: {fmt(card_chg_count)}
Daily Card Charge Amount: {fmt(card_chg_amount)}
*Daily Ticket Sales*
Total Tickets Sale Count: {fmt(ticket_sale_count)}
Total Tickets Sale Amount: {fmt(ticket_sale_amount)}
*QR Mobile*
Total QR Tickets: {fmt(qr_count)}
Total QR Tickets Amount: {fmt(qr_amount)}
*General Statistics - Orange Line Metro*
Date: {date_val}
Day: {day_str}
Total Riders: {fmt(olm_riders)}
Total Revenue: {fmt(olm_revenue)}
Total Sales: {fmt(olm_sales)}
*Grand Total*
Total Ridership Count: {fmt(grand_total_riders)}
Total Sale Amount: {fmt(grand_total_sales)}"""

    st.code(main_template, language=None)

with tab2:
    summary_template = f"""*Ridership Details*
Date: {date_val}
Day: {day_str} 

*Orange Line Metro* = {fmt(olm_riders)}
*Feeder Routes* = {fmt(feeder_routes_riders)}

*Total Ridership* = {fmt(grand_total_riders)}
*Total Sale Amount* = {fmt(grand_total_sales)}"""

    st.code(summary_template, language=None)

st.divider()

# ================= ROW 3: QUICK CONVERTER =================
st.header("Quick Converter")
st.write("Paste your Main Format text here to extract and generate a Short Summary.")

pasted_text = st.text_area("Paste Main Report Here", height=150)

if st.button("Convert to Short Summary", type="primary"):
    if not pasted_text.strip():
        st.warning("Please paste the Main Format text into the box first.")
    else:
        try:
            # Use Regular Expressions to find the needed numbers
            date_match = re.search(r"Date:\s*(.+)", pasted_text)
            day_match = re.search(r"Day:\s*(.+)", pasted_text)
            olm_match = re.search(r"Total Riders:\s*([\d,]+)", pasted_text)
            total_riders_match = re.search(r"Total Ridership Count:\s*([\d,]+)", pasted_text)
            total_sales_match = re.search(r"Total Sale Amount:\s*([\d,\.]+)", pasted_text)

            if not (date_match and olm_match and total_riders_match and total_sales_match and day_match):
                raise ValueError("Missing required fields in pasted text.")

            # Extract the raw strings
            c_date_val = date_match.group(1).strip()
            c_day_val = day_match.group(1).strip()
            c_olm_str = olm_match.group(1)
            c_total_riders_str = total_riders_match.group(1)
            c_total_sales_str = total_sales_match.group(1)

            # Convert riders to integers to calculate the feeder routes
            c_olm_riders = int(c_olm_str.replace(",", ""))
            c_total_riders = int(c_total_riders_str.replace(",", ""))
            
            # Feeder Routes = Grand Total Ridership - Orange Line Riders
            c_feeder_routes = c_total_riders - c_olm_riders

            # Build the new short format
            converted_summary = f"""*Ridership Details*
Date: {c_date_val}
Day: {c_day_val}

*Orange Line Metro* = {c_olm_riders:,}
*Feeder Routes* = {c_feeder_routes:,}

*Total Ridership* = {c_total_riders:,}
*Total Sale Amount* = {c_total_sales_str}"""

            st.success("Converted successfully! Use the copy icon in the top right of the box below.")
            st.code(converted_summary, language=None)

        except Exception as e:
            st.error("Parse Error: Could not understand the pasted text. Please make sure you are pasting the EXACT format generated by the Main Template.")
