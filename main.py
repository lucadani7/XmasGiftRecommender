import os
import pickle

import pandas as pd
import streamlit as st
from sentence_transformers import SentenceTransformer, util

st.set_page_config(page_title="Santa's AI Workshop 🎅", page_icon="❄️", layout="wide")

CURRENCY_RATE = 105.0 # 105 indian rupees ~= 1 euro
EMBEDDINGS_FILE = "amazon_embeddings.pkl"

@st.cache_resource
def get_model():
    return SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


@st.cache_data
def load_and_prepare_data():
    df = pd.read_csv('amazon.csv')
    df['img_link'] = df['img_link'].astype(str).apply(lambda x: x.split('|')[0])
    # euro conversion
    df['price_eur'] = (df['discounted_price'].str.replace('₹', '').str.replace(',', '').astype(float) / CURRENCY_RATE).round(2)
    df['about_product'] = df['about_product'].fillna('')

    # embedding
    if os.path.exists(EMBEDDINGS_FILE):
        with open(EMBEDDINGS_FILE, 'rb') as f:
            embeddings = pickle.load(f)
    else:
        model = get_model()
        # computing vectors only once
        embeddings = model.encode(df['about_product'].str[:500].tolist(), convert_to_tensor=True, show_progress_bar=True)
        with open(EMBEDDINGS_FILE, 'wb') as f:
            pickle.dump(embeddings, f)
    return df, embeddings

model = get_model()
df, corpus_embeddings = load_and_prepare_data()

st.title("🎄 Santa's AI Gift Finder")
st.markdown("### Find the perfect gift using AI!")

st.sidebar.header("Configure Santa Claus's bag")
max_price = st.sidebar.select_slider(
    "Maxim Budget (€)",
    options=[1, 2, 5, 10, 20, 50, 100, 200, 500],
    value=50
)

st.write("Out of inspiration? Try a category:")
c1, c2, c3, c4 = st.columns(4)
q1 = c1.button("🔌 Tech Gadgets")
q2 = c2.button("🍳 Kitchen & Home")
q3 = c3.button("🎧 Music & Audio")
q4 = c4.button("🧸 Toys & Hobby")

search_query = ""
if q1: search_query = "High tech electronics cables and accessories"
if q2: search_query = "Kitchen appliances and home decor"
if q3: search_query = "Wireless headphones and speakers"
if q4: search_query = "Toys for kids and creative hobbies"

user_input = st.text_input("Or describe the person in any language:", value=search_query)
if user_input:
    query_emb = model.encode(user_input, convert_to_tensor=True)
    scores = util.cos_sim(query_emb, corpus_embeddings)[0]
    df['temp_score'] = scores.tolist()
    df_filtered = df[df['price_eur'] <= max_price].copy()
    relevance_threshold = 0.35
    df_filtered = df_filtered[df_filtered['temp_score'] > relevance_threshold]
    results = df_filtered.sort_values(by='temp_score', ascending=False).head(15)
    products_number = len(df[df['price_eur'] <= max_price])
    st.sidebar.write(f"🔍 {products_number} products available within this budget!")

    if results.empty:
        st.warning("Sorry, you don't have enough money to buy this gift!")
    else:
        st.snow()
        st.success(f"Found {len(results)} relevant gifts!")
        cols = st.columns(3)
        for i, (idx, row) in enumerate(results.iterrows()):
            with cols[i % 3]:
                with st.container(border=True):
                    try:
                        st.image(row['img_link'], use_container_width=True)
                    except:
                        st.image(
                            "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Git-logo.svg/1024px-Git-logo.svg.png",
                            use_container_width=True)
                    percentage_score = int(row['temp_score'] * 100)
                    color_score = "green" if percentage_score >= 50 else "orange"
                    st.markdown(f"""
                                            <div style="background-color: #f0f2f6; padding: 5px; border-radius: 5px; text-align: center; margin-bottom: 10px;">
                                                AI match: <span style="color: {color_score}; font-weight: bold;">{percentage_score}%</span>
                                            </div>
                                        """, unsafe_allow_html=True)
                    st.markdown(f"**{row['product_name'][:50]}...**")
                    st.success(f"Price: {row['price_eur']} €")
                    with st.expander("Why this gift?"):
                        st.write(row['about_product'][:300] + "...")