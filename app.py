import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import google.generativeai as genai

# Set your Gemini API Key here
genai.configure(api_key="AIzaSyBwU6KJhVTq1Jw1WI4Yj6ePOAgnKGUkn2k")

# Page Title
st.title("📈 Auto Chart Builder with AI Summary")

# File Upload
uploaded_file = st.file_uploader("Upload your company CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")

    st.subheader("📋 Data Preview")
    st.dataframe(df.head())

    st.subheader("📊 Charts")

    # --- 1. Auto create 5-10 Charts ---
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns

    chart_count = 0

    # Chart 1: Distribution of a numeric column
    if len(numeric_cols) >= 1:
        st.write(f"### Distribution of {numeric_cols[0]}")
        fig, ax = plt.subplots()
        sns.histplot(df[numeric_cols[0]], kde=True, ax=ax)
        st.pyplot(fig)
        chart_count += 1

    # Chart 2: Boxplot of a numeric column
    if len(numeric_cols) >= 2:
        st.write(f"### Boxplot of {numeric_cols[1]}")
        fig, ax = plt.subplots()
        sns.boxplot(x=df[numeric_cols[1]], ax=ax)
        st.pyplot(fig)
        chart_count += 1

    # Chart 3: Countplot of a categorical column
    if len(categorical_cols) >= 1:
        st.write(f"### Count of {categorical_cols[0]}")
        fig, ax = plt.subplots()
        sns.countplot(x=df[categorical_cols[0]], order=df[categorical_cols[0]].value_counts().index, ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)
        chart_count += 1

    # Chart 4: Scatter plot between two numeric columns
    if len(numeric_cols) >= 2:
        st.write(f"### Scatter plot: {numeric_cols[0]} vs {numeric_cols[1]}")
        fig, ax = plt.subplots()
        sns.scatterplot(x=df[numeric_cols[0]], y=df[numeric_cols[1]], ax=ax)
        st.pyplot(fig)
        chart_count += 1

    # Chart 5: Correlation heatmap
    if len(numeric_cols) >= 2:
        st.write("### Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(8,6))
        sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)
        chart_count += 1

    # If less than 5 charts made, create more simple charts
    if chart_count < 5 and len(numeric_cols) >= 3:
        st.write(f"### Line plot of {numeric_cols[2]}")
        fig, ax = plt.subplots()
        df[numeric_cols[2]].plot(ax=ax)
        st.pyplot(fig)
        chart_count += 1

    st.success(f"✅ Created {chart_count} charts automatically!")

    # --- 2. Create Summary using Gemini AI ---

    st.subheader("🧠 AI Summary")

    # Prepare data for Gemini
    prompt = f"""
    Analyze the following company dataset columns: {list(df.columns)}
    and the charts generated: {chart_count} charts.

    Give a short business summary about what insights a company can get from these charts.
    """

    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content(prompt)

    st.write(response.text)