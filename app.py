import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="PCB Gift Calculator", page_icon="🌴", layout="wide")

# --- DATA DATABASE ---
# Updated to use "type": "money" for items where you type a dollar amount.
DB = {
    "Attractions": {
        "Just Jump": {
            "notes": "1 hour jump. Expiration: 10 Days.",
            "variants": [
                {"name": "Adult (7 and over)", "m_cost": 14.36, "r_cost": 20.52},
                {"name": "Child (6 and under)", "m_cost": 10.96, "r_cost": 15.66},
            ]
        },
        "Wonderworks": {
            "notes": "General Admission. We do not issue tickets - Do not add to Journey.",
            "variants": [
                {"name": "Adult (13-59)", "m_cost": 28.00, "r_cost": 37.81},
                {"name": "Child (5-12)", "m_cost": 23.00, "r_cost": 31.33},
                {"name": "Senior (60+)", "m_cost": 23.00, "r_cost": 31.33},
            ]
        },
        "Sky Wheel": {
            "notes": "Does not include Ropes/Mini Golf. 1 Flight. We do not issue tickets.",
            "variants": [
                {"name": "Adult (12 and over)", "m_cost": 14.00, "r_cost": 19.02},
                {"name": "Child (5-11)", "m_cost": 10.00, "r_cost": 15.02},
            ]
        },
        "Race City": {
            "notes": "Race City PCB - GA. 10 Days from Tour.",
            "variants": [
                {"name": "General Admission", "m_cost": 10.00, "r_cost": 14.25},
            ]
        },
        "Mini Golf (Skywheel)": {
            "notes": "18 Hole Mini Golf - GA.",
            "variants": [
                {"name": "General Admission", "m_cost": 11.00, "r_cost": 16.04},
            ]
        },
        "Gulf World": {
            "notes": "Exclusions: Encounters and Swims. General Admission. We do not issue tickets.",
            "variants": [
                {"name": "Ages 5 and over", "m_cost": 20.00, "r_cost": 27.00},
            ]
        },
        "Shipwreck Island": {
            "notes": "General Admission - Separate Scan VIP line for entrance. We do not issue tickets.",
            "variants": [
                {"name": "Adult (50 inches +)", "m_cost": 49.99, "r_cost": 51.53},
                {"name": "Child (35-50 inches)", "m_cost": 39.99, "r_cost": 41.22},
                {"name": "Senior 62+", "m_cost": 36.99, "r_cost": 38.13},
            ]
        },
        "Pirates Voyage": {
            "notes": "Pirates Voyage PCB - GA.",
            "variants": [
                {"name": "Adult", "m_cost": 71.00, "r_cost": 79.91},
                {"name": "Child", "m_cost": 37.00, "r_cost": 42.46},
            ]
        },
        "Duplin Winery": {
            "notes": "Must be 21 or older.",
            "variants": [
                {"name": "Wine Tasting", "m_cost": 10.00, "r_cost": 17.12},
            ]
        }
    },
    "Tours & Cruises": {
        "Cruisin Tikis": {
            "notes": "10 Days from tour.",
            "variants": [
                {"name": "3 Hour Sand Bar Cruise", "m_cost": 60.00, "r_cost": 86.00},
                {"name": "1.5 Hour Lit on the Lagoon", "m_cost": 49.00, "r_cost": 69.88},
                {"name": "1.5 Hour Lagoon Cruise", "m_cost": 42.00, "r_cost": 59.13},
                {"name": "1.5 Sunset Cruise", "m_cost": 49.00, "r_cost": 69.88},
            ]
        },
        "Capt Anderson Marina": {
            "notes": "6 Hour Fishing Trip. 10 Day from tour.",
            "variants": [
                {"name": "Fishing Trip", "m_cost": 91.49, "r_cost": 101.65},
            ]
        },
        "Paradise Adventures": {
            "notes": "Expiration: 2 Weeks.",
            "variants": [
                {"name": "Sail Evening Sunset", "m_cost": 30.00, "r_cost": 45.00},
                {"name": "Sail Half Day Excursion", "m_cost": 50.00, "r_cost": 75.00},
            ]
        },
        "Grandmere Shell Island": {
            "notes": "Guest must call resv line to book after tour. 3.5 hrs Air conditioned double decker boat. Cash Bar.",
            "variants": [
                {"name": "Dolphin Watch Adult (13+)", "m_cost": 26.00, "r_cost": 38.00},
                {"name": "Dolphin Watch Child (3-12)", "m_cost": 17.00, "r_cost": 24.00},
                {"name": "Sunset Cruise Adult (13+)", "m_cost": 19.00, "r_cost": 28.00},
                {"name": "Sunset Cruise Child (3-12)", "m_cost": 14.00, "r_cost": 19.00},
            ]
        }
    },
    "Restaurants & Gifts": {
        "Restaurant Cards": {
            "notes": "Enter the Retail Value ($). Cost is calculated automatically.",
            "variants": [
                {"name": "Capt Anderson's", "type": "money", "ratio": 0.8},
                {"name": "FireFly", "type": "money", "ratio": 0.8},
                {"name": "Sharky's", "type": "money", "ratio": 0.8},
                {"name": "HammerHead Fred's", "type": "money", "ratio": 0.8},
                {"name": "Runaway Island", "type": "money", "ratio": 0.8},
                {"name": "Multi-Rest Card", "type": "money", "ratio": 0.85},
                {"name": "Dick's Last Resort", "type": "money", "ratio": 0.8},
                {"name": "Dave & Buster's", "type": "money", "ratio": 0.5},
            ]
        },
        "Margaritaville": {
            "notes": "Enter total amount. Cost is 50%.",
            "variants": [
                {"name": "Gift Card Amount", "type": "money", "ratio": 0.5},
            ]
        },
        "Tango Rewards": {
            "notes": "No Cash Cards. Max $175 retail cost.",
            "variants": [
                {"name": "Tango Link Amount", "type": "money", "ratio": 1.0},
            ]
        }
    },
    "Points & Incentives": {
        "Wyndham Rewards": {
            "notes": "Good for hotels and resorts. No taxes/fees, no blackout. (Retail estimated @ $10/1k pts)",
            "variants": [
                {"name": "1,000 Points", "m_cost": 5.13, "r_cost": 10.00},
                {"name": "15,000 Points", "m_cost": 77.00, "r_cost": 150.00},
                {"name": "30,000 Points", "m_cost": 154.00, "r_cost": 300.00},
                {"name": "45,000 Points", "m_cost": 231.00, "r_cost": 450.00},
            ]
        },
        "Vacations": {
            "notes": "Not for use in PCB. 4500 Resorts, no black outs but meant for off peak travel.",
            "variants": [
                {"name": "8/7 Vacation (Endless)", "m_cost": 75.00, "r_cost": 1499.00},
                {"name": "Vacation Pass", "m_cost": 0.00, "r_cost": 1098.00},
                {"name": "RCI Getaway", "m_cost": 75.00, "r_cost": 1499.00},
            ]
        },
        "Tru Incentive": {
            "notes": "Not transferable. Taxes and fees apply.",
            "variants": [
                {"name": "3,4,5 Night Cruise", "m_cost": 75.00, "r_cost": 1550.00},
                {"name": "4,5,7 Night Cruise", "m_cost": 75.00, "r_cost": 1975.00},
                {"name": "7 Night Resort Condo", "m_cost": 75.00, "r_cost": 2100.00},
            ]
        }
    }
}

# --- INITIALIZE SESSION STATE ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'max_budget' not in st.session_state:
    st.session_state.max_budget = 200.00
if 'marketer_cost_input' not in st.session_state:
    st.session_state.marketer_cost_input = 0.0
if 'last_cart_total' not in st.session_state:
    st.session_state.last_cart_total = 0.0

# --- FUNCTIONS ---
def add_to_cart(item_name, variant_name, m_cost, r_cost, qty):
    if qty > 0:
        st.session_state.cart.append({
            "Item": item_name,
            "Variant": variant_name,
            "Marketer Cost": m_cost,
            "Retail Cost": r_cost,
            "Qty": qty,
            "Total M": m_cost * qty,
            "Total R": r_cost * qty
        })

def clear_cart():
    st.session_state.cart = []
    st.session_state.marketer_cost_input = 0.0
    st.session_state.last_cart_total = 0.0

# --- TOP DASHBOARD (THE MONEY ZONE) ---
st.title("🎟️ PCB Gift Calculator")

raw_m_cost = sum(item['Total M'] for item in st.session_state.cart)
total_r_cost = sum(item['Total R'] for item in st.session_state.cart)

col1, col2, col3 = st.columns(3)

with col1:
    st.session_state.max_budget = st.number_input(
        "Max Budget (Company)", 
        value=st.session_state.max_budget, 
        step=10.0
    )

with col2:
    if raw_m_cost != st.session_state.last_cart_total:
        new_default = min(raw_m_cost, st.session_state.max_budget)
        st.session_state.marketer_cost_input = new_default
        st.session_state.last_cart_total = raw_m_cost

    marketer_pay_input = st.number_input(
        "Marketer Cost (You Pay)", 
        key="marketer_cost_input", 
        step=1.0,
        help="Type the amount you want to pay. Guest pays the rest."
    )
    
    if raw_m_cost > 0:
        calculated_guest_pay = raw_m_cost - marketer_pay_input
        guest_pays = max(75.0, calculated_guest_pay)
        effective_marketer_pay = raw_m_cost - guest_pays
    else:
        guest_pays = 0.0
        effective_marketer_pay = 0.0

    if effective_marketer_pay < marketer_pay_input:
        st.caption(f"🔒 Adjusted to **${effective_marketer_pay:,.2f}** (Guest Min $75)")
    
    if effective_marketer_pay > st.session_state.max_budget:
         st.caption(f"⚠️ Over Budget")

with col3:
    st.metric("Guest Pays", f"${guest_pays:,.2f}")
    if guest_pays == 75.0 and raw_m_cost > 0:
        st.caption("🔒 Min. Payment Applied")
    st.markdown(f"<div style='text-align: right; color: gray; font-size: 0.8em;'>Cart Value: ${raw_m_cost:,.2f}</div>", unsafe_allow_html=True)

st.divider()

# --- MAIN SELECTION AREA ---
st.header("Build Package")

category = st.selectbox("Select Category", list(DB.keys()))
item_name = st.selectbox("Select Attraction/Item", list(DB[category].keys()))
selected_item = DB[category][item_name]

if selected_item['notes']:
    st.info(f"ℹ️ **NOTE:** {selected_item['notes']}")

with st.form("add_form", clear_on_submit=True):
    # Dictionaries to store inputs
    input_values = {}
    
    if item_name == "Restaurant Cards":
        st.caption("Enter the dollar amount you want to give.")

    for variant in selected_item['variants']:
        c1, c2, c3 = st.columns([3, 2, 2])
        
        # Check if this is a "Money" input item
        is_money_type = variant.get('type') == 'money'
        
        with c1:
            st.write(f"**{variant['name']}**")
        with c2:
            if is_money_type:
                # Show ratio for clarity (e.g. "Cost: 80%")
                pct = int(variant['ratio'] * 100)
                st.caption(f"Cost: {pct}% of Retail")
            else:
                st.caption(f"M: ${variant['m_cost']} | R: ${variant['r_cost']}")
        with c3:
            # Render different inputs based on type
            key_id = f"{item_name}_{variant['name']}"
            if is_money_type:
                input_values[variant['name']] = st.number_input(
                    "Amount ($)", min_value=0.0, value=0.0, step=5.0, key=key_id, label_visibility="collapsed"
                )
            else:
                input_values[variant['name']] = st.number_input(
                    "Qty", min_value=0, value=0, key=key_id, label_visibility="collapsed"
                )

    submitted = st.form_submit_button("Add to Cart", type="primary")

    if submitted:
        any_added = False
        for variant in selected_item['variants']:
            val = input_values[variant['name']]
            
            if val > 0:
                if variant.get('type') == 'money':
                    # Special logic for Money items
                    # m_cost is calculated dynamically based on input * ratio
                    # r_cost is the input itself
                    # qty is 1 (representing "1 custom value")
                    calc_m = val * variant['ratio']
                    display_name = f"{variant['name']} (Val: ${val:.0f})"
                    add_to_cart(item_name, display_name, calc_m, val, 1)
                else:
                    # Standard logic for Tickets
                    add_to_cart(item_name, variant['name'], variant['m_cost'], variant['r_cost'], val)
                
                any_added = True
        
        if any_added:
            st.success(f"Added {item_name} to cart!")
            st.rerun()
        else:
            st.warning("Please enter a value greater than 0.")
            
st.divider()

# --- BOTTOM SUMMARY (THE RECEIPT) ---
st.header("Current Package")

if len(st.session_state.cart) > 0:
    for i, item in enumerate(st.session_state.cart):
        col1, col2, col3 = st.columns([5, 2, 1])
        with col1:
            st.write(f"**{item['Item']}**")
            st.caption(f"{item['Variant']}")
        with col2:
            st.write(f"Qty: {item['Qty']}")
            st.write(f"${item['Total M']:.2f}")
        with col3:
            if st.button("🗑️", key=f"remove_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
        st.divider()

    st.markdown(f"""
        <div style="background-color: #d4edda; padding: 20px; border-radius: 10px; text-align: center; border: 2px solid #28a745;">
            <h2 style="color: #155724; margin:0;">Total Retail Value: ${total_r_cost:,.2f}</h2>
            <p style="color: #155724; margin:0;">(Value to Guest)</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("") 
    if st.button("Clear All / New Guest", type="secondary"):
        clear_cart()
        st.rerun()

else:
    st.info("Cart is empty. Select items above to start.")
