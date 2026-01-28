import streamlit as st
import pandas as pd

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="PCB Gift Calculator", page_icon="🌴", layout="wide")

# --- DATA DATABASE ---
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
        }
    },
    "Vacations & Points": {
        "Vacation Packages": {
            "notes": "Major trips and getaways. See restrictions.",
            "variants": [
                {"name": "8/7 Resort Stay", "m_cost": 75.00, "r_cost": 1499.00},
                {"name": "Cruise (3-5 Night)", "m_cost": 75.00, "r_cost": 1550.00},
                {"name": "Vacation Pass", "m_cost": 0.00, "r_cost": 1098.00},
                {"name": "Resort Condo (7 Night)", "m_cost": 75.00, "r_cost": 2100.00},
            ]
        },
        "Wyndham Rewards": {
            "notes": "Good for hotels and resorts. Retail estimated @ $10/1k pts.",
            "variants": [
                {"name": "1,000 Points", "m_cost": 5.13, "r_cost": 10.00},
                {"name": "15,000 Points", "m_cost": 77.00, "r_cost": 150.00},
                {"name": "30,000 Points", "m_cost": 154.00, "r_cost": 300.00},
                {"name": "45,000 Points", "m_cost": 231.00, "r_cost": 450.00},
            ]
        },
        "Tango Rewards": {
            "notes": "No Cash Cards. Max $175 retail cost.",
            "variants": [
                {"name": "Tango Link Amount", "type": "money", "ratio": 1.0},
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
    # Also clear any form inputs that might be lingering
    for key in list(st.session_state.keys()):
        if key.startswith("input_"):
            st.session_state[key] = 0.0

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
        key="marketer_cost
