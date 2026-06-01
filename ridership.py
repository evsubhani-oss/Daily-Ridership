# -*- coding: utf-8 -*-
"""
Created on Mon Jun  1 14:33:37 2026

@author: Subhani
"""

import streamlit as st
from datetime import datetime, timedelta
import re

# --- Setup Page ---
st.set_page_config(page_title="Transport Stats Generator", layout="wide")
st.title("Transport Stats (Web Version with Converter)")

# --- Helper Functions ---
def get_val(val_str, is_float=False):
    """Safely gets number from string input."""
    raw = val_str.replace(",", "").strip()
    try:
        if is_float:
            return float(raw)
        return int(float(raw))
    except ValueError:
        return 0

def fmt(number):
    """Formats number with commas."""
    return f"{number:,.0f}" if isinstance(number, int) or number.is_integer() else f"{number:,.2f}"

# --- Initialize Session State for Outputs ---
if "main_output" not in st.session_state:
    st.session_state.main_output = ""
if "short_output" not in st.session_state:
    st.session_state.short_output = ""
if "converter_output" not in st.session_state:
    st.session_state.converter_output = ""

# --- ROW 1: Date & Day ---
st.subheader("Date Selection")
yesterday = datetime.now() - timedelta(days=1)
yesterday_str = yesterday.strftime("%Y-%m-%d")
day_str = yesterday.strftime("%A")

top_col1, top_col2, _ = st.columns([1, 1, 4])
with top_col1:
    date_val = st.text_input("Date (YYYY-MM-DD):", value=yesterday_str)
with top_col2:
    # Auto-update day logic if date is valid
    try:
        dt = datetime.strptime(date_val, "%Y-%m-%d")
        day_str = dt.strftime("%A")
    except ValueError:
        pass
    day_val = st.text_input("Day:", value=day_str)

st.markdown("---")

# --- ROW 2: Data Inputs (3 Columns) ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Daily Boarding**")
    ev_daily_count = st.text_input("Daily Count:", key="ev_count")
    ev_daily_amount = st.text_input("Daily Amount:", key="ev_amt")
    
    st.markdown("**Daily Bus Count**")
    total_bus = st.text_input("Total Bus:", value="180", key="tot_bus")
    working_bus = st.text_input("Working Buses:", key="work_bus")
    
    st.markdown("**MST Card Charge**")
    mst_count = st.text_input("Charge Count:", key="mst_c")
    mst_amount = st.text_input("Charge Amount:", key="mst_amt")
    mst_balance = st.text_input("Balance Amount:", value="0.00", key="mst_bal")

with col2:
    st.markdown("**Daily Card Charge**")
    card_chg_count = st.text_input("Charge Count:", key="card_c")
    card_chg_amount = st.text_input("Charge Amount:", key="card_amt")
    
    st.markdown("**Daily Ticket Sales**")
    ticket_sale_count = st.text_input("Ticket Sale Count:", key="tkt_c")
    ticket_sale_amount = st.text_input("Ticket Sale Amount:", key="tkt_amt")
    
    st.markdown("**QR Mobile**")
    qr_count = st.text_input("Total QR Tickets:", key="qr_c")

with col3:
    st.markdown("**Orange Line Metro**")
    olm_riders = st.text_input("Total Riders:", key="olm_riders")
    olm_revenue = st.text_input("Total Revenue:", key="olm_rev")
    olm_sales = st.text_input("Total Sales:", key="olm_sales")
    
    st.markdown("---")
    
    # Collect all inputs in a dictionary for validation
    inputs_dict = {
        "Daily Count": ev_daily_count, "Daily Amount": ev_daily_amount,
        "Total Bus": total_bus, "Working Buses": working_bus,
        "MST Charge Count": mst_count, "MST Charge Amount": mst_amount, "MST Balance": mst_balance,
        "Card Charge Count": card_chg_count, "Card Charge Amount": card_chg_amount,
        "Ticket Sale Count": ticket_sale_count, "Ticket Sale Amount": ticket_sale_amount,
        "QR Tickets": qr_count,
        "OLM Riders": olm_riders, "OLM Revenue": olm_revenue, "OLM Sales": olm_sales
    }
    
    def check_empty_fields():
        empty = [k for k, v in inputs_dict.items() if not v.strip()]
        if empty:
            st.warning(f"Missing Values for: {', '.join(empty)}.\nPlease enter 0 if there is no data.")
            return False
        return True

    def calculate_data():
        d = {}
        d['ev_daily_count'] = get_val(ev_daily_count)
        d['ev_daily_amount'] = get_val(ev_daily_amount, True)
        d['total_bus'] = get_val(total_bus)
        d['working_bus'] = get_val(working_bus)
        d['mst_count'] = get_val(mst_count)
        d['mst_amount'] = get_val(mst_amount, True)
        d['mst_balance'] = get_val(mst_balance, True)
        d['card_chg_count'] = get_val(card_chg_count)
        d['card_chg_amount'] = get_val(card_chg_amount, True)
        d['ticket_sale_count'] = get_val(ticket_sale_count)
        d['ticket_sale_amount'] = get_val(ticket_sale_amount, True)
        d['qr_count'] = get_val(qr_count)
        d['olm_riders'] = get_val(olm_riders)
        d['olm_revenue'] = get_val(olm_revenue, True)
        d['olm_sales'] = get_val(olm_sales, True)

        d['qr_amount'] = d['qr_count'] * 50
        d['grand_total_riders'] = d['olm_riders'] + d['qr_count'] + d['ticket_sale_count']
        d['grand_total_sales'] = d['olm_sales'] + d['qr_amount'] + d['ticket_sale_amount']
        d['feeder_routes_riders'] = d['qr_count'] + d['ticket_sale_count']
        return d

    # Buttons
    if st.button("GENERATE MAIN TEMPLATE", use_container_width=True):
        if check_empty_fields():
            d = calculate_data()
            st.session_state.main_output = f"""*General Statistics - EV & HEV Buses*
Date: {date_val}
Day: {day_val}
*Daily Boarding*
Daily Count: {fmt(d['ev_daily_count'])}
Daily Amount: {fmt(d['ev_daily_amount'])}
*Daily Bus Count*
Total Bus: {fmt(d['total_bus'])}
Working Buses: {fmt(d['working_bus'])}
*Daily MST Card Charge Info*
MST Card Charge Count: {fmt(d['mst_count'])}
MST Card Charge Amount: {fmt(d['mst_amount'])}
MST Card Balance Amount: {fmt(d['mst_balance'])}
*Daily Card Charge*
Daily Card Charge Count: {fmt(d['card_chg_count'])}
Daily Card Charge Amount: {fmt(d['card_chg_amount'])}
*Daily Ticket Sales*
Total Tickets Sale Count: {fmt(d['ticket_sale_count'])}
Total Tickets Sale Amount: {fmt(d['ticket_sale_amount'])}
*QR Mobile*
Total QR Tickets: {fmt(d['qr_count'])}
Total QR Tickets Amount: {fmt(d['qr_amount'])}
*General Statistics - Orange Line Metro*
Date: {date_val}
Day: {day_val}
Total Riders: {fmt(d['olm_riders'])}
Total Revenue: {fmt(d['olm_revenue'])}
Total Sales: {fmt(d['olm_sales'])}
*Grand Total*
Total Ridership Count: {fmt(d['grand_total_riders'])}
Total Sale Amount: {fmt(d['grand_total_sales'])}"""

    if st.button("GENERATE SHORT SUMMARY", use_container_width=True):
        if check_empty_fields():
            d = calculate_data()
            st.session_state.short_output = f"""*Ridership Details*
Date: {date_val}

*Orange Line Metro* = {fmt(d['olm_riders'])}
*Feeder Routes* = {fmt(d['feeder_routes_riders'])}

*Total Ridership* = {fmt(d['grand_total_riders'])}
*Total Sale Amount* = {fmt(d['grand_total_sales'])}"""

    if st.session_state.main_output:
        st.markdown("**Main Output:** *(Hover over box & click top-right icon to copy)*")
        st.code(st.session_state.main_output, language="markdown")

    if st.session_state.short_output:
        st.markdown("**Short Output:** *(Hover over box & click top-right icon to copy)*")
        st.code(st.session_state.short_output, language="markdown")

st.markdown("---")

# --- ROW 3: Quick Converter ---
st.subheader("Quick Converter (Paste Main Format Here to Get Short Summary)")
paste_text = st.text_area("Paste text generated from Main Template here:", height=150)

if st.button("CONVERT TO SHORT SUMMARY"):
    if not paste_text.strip():
        st.warning("Please paste the Main Format text into the box first.")
    else:
        try:
            date_match = re.search(r"Date:\s*(.+)", paste_text)
            olm_match = re.search(r"Total Riders:\s*([\d,]+)", paste_text)
            total_riders_match = re.search(r"Total Ridership Count:\s*([\d,]+)", paste_text)
            total_sales_match = re.search(r"Total Sale Amount:\s*([\d,\.]+)", paste_text)
            
            if not (date_match and olm_match and total_riders_match and total_sales_match):
                raise ValueError("Missing fields")

            # Extract raw strings
            c_date_val = date_match.group(1).strip()
            olm_str = olm_match.group(1)
            total_riders_str = total_riders_match.group(1)
            total_sales_str = total_sales_match.group(1)

            # Convert riders to integers for math
            c_olm_riders = int(olm_str.replace(",", ""))
            c_total_riders = int(total_riders_str.replace(",", ""))
            
            # Feeder Routes = Grand Total Ridership - Orange Line Riders
            c_feeder_routes = c_total_riders - c_olm_riders

            # Output Template
            st.session_state.converter_output = f"""*Ridership Details*
Date: {c_date_val}

*Orange Line Metro* = {c_olm_riders:,}
*Feeder Routes* = {c_feeder_routes:,}

*Total Ridership* = {c_total_riders:,}
*Total Sale Amount* = {total_sales_str}"""
            
            st.success("Successfully converted!")
        except Exception as e:
            st.error("Could not parse text. Ensure you pasted the exact Main Template format.")

if st.session_state.converter_output:
    st.markdown("**Converted Short Summary:** *(Hover over box & click top-right icon to copy)*")
    st.code(st.session_state.converter_output, language="markdown")