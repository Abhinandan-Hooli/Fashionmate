# app.py
import os
import json
from typing import List, Optional, Dict, Any
import streamlit as st

# ---------------------------
# Replace / import your real products dataset here.
# For demo, a small sample list; replace with real 'products' from your data module.
# ---------------------------
products = [
    {
        "ProductID": "101",
        "ProductName": "Linen Summer Shirt",
        "ProductBrand": "Breeze",
        "PrimaryColor": "#F6E6E6",
        "Description": "Lightweight linen shirt, breathable for warm days.",
        "Price": 1299
    },
    {
        "ProductID": "102",
        "ProductName": "Slim Fit Jeans",
        "ProductBrand": "DenimCo",
        "PrimaryColor": "#1F2937",
        "Description": "Classic slim fit blue jeans with stretch.",
        "Price": 1999
    },
    {
        "ProductID": "103",
        "ProductName": "White Sneakers",
        "ProductBrand": "StepUp",
        "PrimaryColor": "#FFFFFF",
        "Description": "Crisp white low-top sneakers.",
        "Price": 2499
    },
    {
        "ProductID": "104",
        "ProductName": "Leather Crossbody Bag",
        "ProductBrand": "CarryAll",
        "PrimaryColor": "#8B5E3C",
        "Description": "Compact leather bag with adjustable strap.",
        "Price": 3499
    },
    # add your full inventory here...
]

# ---------------------------
# Helper types & functions
# ---------------------------
def get_product_by_id(prod_id: str) -> Optional[Dict[str, Any]]:
    if prod_id == "NONE" or prod_id is None:
        return None
    return next((p for p in products if str(p.get("ProductID")) == str(prod_id)), None)

# ---------------------------
# AI call: stub + example
# ---------------------------
def call_genai(prompt: str) -> Dict[str, Any]:
    """
    Call your Generative AI model to get a JSON response matching the schema:
    {
      "top_id": "101",
      "bottom_id": "102",
      "footwear_id": "103",
      "accessory_id": "104",
      "style_tags": ["casual", "summer", "minimal"],
      "color_palette": ["#FFFFFF", "#1F2937", "#8B5E3C"],
      "reasoning": "This outfit works because ...",
      "occasion_title": "Summer Garden Casual"
    }

    THIS FUNCTION IS A STUB. Replace with real code that calls Google GenAI or your preferred LLM.
    Example (pseudo) with Google GenAI Python client (you must adapt to the actual client API):
    
    from google.generativeai import Client
    client = Client(api_key=API_KEY)
    response = client.generate_text(
      model="gemini-2.5-flash",
      prompt=prompt,
      max_output_tokens=512,
      temperature=0.2,
      content_type="application/json"
    )
    return json.loads(response.text)

    If you don't have an API key set, this function returns a mocked response for testing.
    """
    # Try to read API key — if not present, return a mock.
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("API_KEY")
    if not api_key:
        # Mock response — useful for UI testing without network.
        mock = {
            "top_id": "101",
            "bottom_id": "102",
            "footwear_id": "103",
            "accessory_id": "104",
            "style_tags": ["casual", "summer", "minimal"],
            "color_palette": ["#F6E6E6", "#1F2937", "#8B5E3C"],
            "reasoning": "Light fabrics and neutral colors keep the look airy and cohesive for a garden party.",
            "occasion_title": "Summer Garden Casual"
        }
        return mock

    # If you want, implement the call using your SDK here.
    # For safety and forward-compatibility I leave this as a placeholder so you can plug-in your preferred client.
    raise RuntimeError("API key present but `call_genai` is not implemented. Please add code to call your GenAI client.")

# ---------------------------
# Build the UI with Streamlit
# ---------------------------
st.set_page_config(page_title="FashionMate", layout="centered")

# Header
with st.container():
    c1, c2 = st.columns([1, 4])
    with c1:
        st.markdown("<div style='font-size:28px; font-family: serif; color:#111827'><strong>FashionMate<span style='color:#FB7185'>.</span></strong></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div style='color:#6B7280; margin-top:8px'>AI Personal Styling Engine</div>", unsafe_allow_html=True)

st.write("---")

# Input section
st.header("What are you dressing for today?")
st.write("From casual brunches to evening galas, describe your occasion and let our AI curate the perfect look from our collection.")

query = st.text_input("Describe the occasion", placeholder="e.g., A chic outfit for a summer garden party...")
col1, col2 = st.columns([1, 4])
with col1:
    pass
with col2:
    submit = st.button("Style Me")

# Error and recommendation placeholders
error_msg = None
recommendation = None

if submit and query.strip():
    with st.spinner("Creating your look..."):
        try:
            # Build inventory context (simplified to save token usage)
            inventory_context = "\n".join([
                f"ID: {p['ProductID']}, Name: {p['ProductName']}, Brand: {p['ProductBrand']}, Color: {p['PrimaryColor']}, Desc: {p['Description']}"
                for p in products
            ])
            prompt = f"""
You are FashionMate, an elite high-fashion AI stylist.

The user needs an outfit for: "{query}"

Select the best matching items from the provided INVENTORY list below to create a complete, stylish outfit.
You MUST pick exactly one 'top' (shirt/t-shirt/kurta/dress), one 'bottom' (jeans/trousers/skirt/shorts/leggings), one 'footwear', and one 'accessory' (watch/bag/jewellery/belt) from the inventory.
If the user selects a dress or jumpsuit (which covers both top and bottom), set the 'bottom_id' to "NONE" or select a complementary legging if appropriate.

INVENTORY:
{inventory_context}

Return a JSON object. Do not include markdown code blocks.
"""
            raw = call_genai(prompt)
            # raw should be dict-like; if string, try parse
            if isinstance(raw, str):
                try:
                    raw = json.loads(raw)
                except Exception:
                    raise ValueError("AI returned non-JSON text.")
            recommendation = raw

        except Exception as e:
            error_msg = f"AI Error: {str(e)}"

# Display error
if error_msg:
    st.error(error_msg)

# Display recommendation
if recommendation:
    st.markdown("### Your Curated Look")
    st.markdown(f"#### {recommendation.get('occasion_title','Untitled Look')}")
    tags = recommendation.get("style_tags", [])
    if tags:
        tag_str = " ".join([f"`{t}`" for t in tags])
        st.markdown(f"{tag_str}")

    # Products grid (4 columns)
    top = get_product_by_id(recommendation.get("top_id"))
    bottom = get_product_by_id(recommendation.get("bottom_id"))
    footwear = get_product_by_id(recommendation.get("footwear_id"))
    accessory = get_product_by_id(recommendation.get("accessory_id"))

    cols = st.columns(4)
    items = [("Top", top), ("Bottom", bottom), ("Footwear", footwear), ("Accessory", accessory)]
    for col, (label, prod) in zip(cols, items):
        with col:
            st.markdown(f"**{label}**")
            if not prod:
                st.info(f"No {label} selected")
            else:
                st.markdown(f"**{prod['ProductName']}**")
                st.markdown(f"*{prod['ProductBrand']}*")
                st.write(prod['Description'])
                st.markdown(f"**₹{prod['Price']}**")
                # color dot
                color = prod.get("PrimaryColor", "#E5E7EB")
                st.markdown(
                    f"<div style='width:36px;height:36px;border-radius:9999px;background:{color};border:1px solid #E6E7EA;margin-top:8px'></div>",
                    unsafe_allow_html=True
                )

    st.write("---")
    st.subheader("Stylist's Note")
    st.info(recommendation.get("reasoning", ""))

    st.subheader("Color Palette")
    palette = recommendation.get("color_palette", [])
    if palette:
        cols = st.columns(len(palette))
        for c, color in zip(cols, palette):
            with c:
                st.markdown(
                    f"<div style='width:72px;height:72px;border-radius:9999px;background:{color};border:1px solid #E6E7EA'></div>",
                    unsafe_allow_html=True
                )
                st.caption(color)
    else:
        st.write("No palette provided.")

    # Raw JSON (collapsible)
    with st.expander("Show raw AI JSON"):
        st.json(recommendation)

# Footer
st.write("---")
st.markdown("Powered by Google Gemini • Fashion dataset included")
