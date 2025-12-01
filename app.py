#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Books Analytics Dashboard")
st.write("Explore book ratings, languages, and popularity using the filters below.")

@st.cache_data
def load_data():
    df = pd.read_csv("books (2).csv", on_bad_lines="skip")
    df = df.rename(columns={"  num_pages": "num_pages"})
    return df

df = load_data()

st.subheader("Raw Data (first 500 rows)")
st.dataframe(df.head(500))

st.sidebar.header("Filters")

if "language_code" in df.columns:
    languages = sorted(df["language_code"].dropna().unique())
    selected_languages = st.sidebar.multiselect(
        "Language code",
        options=languages,
        default=languages
    )
else:
    selected_languages = None

df_filtered = df.copy()
if selected_languages is not None and len(selected_languages) > 0:
    df_filtered = df_filtered[df_filtered["language_code"].isin(selected_languages)]

if "average_rating" in df_filtered.columns:
    min_rating = float(df_filtered["average_rating"].min())
    max_rating = float(df_filtered["average_rating"].max())
    rating_range = st.sidebar.slider(
        "Average rating between",
        min_value=round(min_rating, 1),
        max_value=round(max_rating, 1),
        value=(round(min_rating, 1), round(max_rating, 1)),
        step=0.1
    )
    df_filtered = df_filtered[
        (df_filtered["average_rating"] >= rating_range[0]) &
        (df_filtered["average_rating"] <= rating_range[1])
    ]

st.subheader("Filtered Data")
st.write(f"Number of books: {len(df_filtered)}")
columns_to_show = [c for c in ["title", "authors", "average_rating", "num_pages", "ratings_count", "language_code"] if c in df_filtered.columns]
st.dataframe(df_filtered[columns_to_show])

numeric_cols = [c for c in ["average_rating", "num_pages", "ratings_count", "text_reviews_count"] if c in df_filtered.columns]

if len(numeric_cols) > 0:
    selected_num_col = st.selectbox(
        "Select numeric column to plot histogram",
        options=numeric_cols
    )

    st.subheader(f"Histogram of {selected_num_col}")
    fig, ax = plt.subplots()
    ax.hist(df_filtered[selected_num_col].dropna(), bins=30)
    ax.set_xlabel(selected_num_col)
    ax.set_ylabel("Count")
    st.pyplot(fig)

if "average_rating" in df_filtered.columns and "ratings_count" in df_filtered.columns:
    st.subheader("Top 10 Highest Rated Books (by average rating)")
    top_books = df_filtered.sort_values(["average_rating", "ratings_count"], ascending=[False, False]).head(10)
    st.dataframe(top_books[["title", "authors", "average_rating", "ratings_count"]])

if len(numeric_cols) > 0:
    st.subheader("Summary Statistics")
    st.write(df_filtered[numeric_cols].describe())

