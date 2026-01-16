import streamlit as st
import pickle
import numpy as np
import os

st.set_page_config(
    page_title="Book Recommender",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Book Recommendation System")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "backend", "models")

popular_df = pickle.load(open(os.path.join(MODEL_DIR, "popular.pkl"), "rb"))
pt = pickle.load(open(os.path.join(MODEL_DIR, "pt.pkl"), "rb"))
books = pickle.load(open(os.path.join(MODEL_DIR, "books.pkl"), "rb"))
similarity_scores = pickle.load(open(os.path.join(MODEL_DIR, "similarity_scores.pkl"), "rb"))


# ---------------- Popular Books ----------------
st.subheader("🔥 Popular Books")

num_items = min(5, len(popular_df))
cols = st.columns(num_items)

for i, (_, row) in enumerate(popular_df.head(num_items).iterrows()):
    with cols[i]:
        st.image(row["Image-URL-M"], width=130)
        st.caption(row["Book-Title"])
        st.caption(f"⭐ {round(row['avg_rating'], 2)}")

st.divider()

# ---------------- Recommendation ----------------
st.subheader("🤝 Recommend Similar Books")

selected_book = st.selectbox("Select a Book", pt.index.tolist())

if st.button("Recommend"):
    index = np.where(pt.index == selected_book)[0][0]
    scores = sorted(
        list(enumerate(similarity_scores[index])),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    cols = st.columns(len(scores))
    for col, (idx, _) in zip(cols, scores):
        title = pt.index[idx]
        book = books[books["Book-Title"] == title].iloc[0]

        with col:
            st.image(book["Image-URL-M"], width=130)
            st.caption(book["Book-Title"])
            st.caption(book["Book-Author"])
