import os
import streamlit as st
import plotly.express as px
from datetime import datetime
from dateutil import parser
import openai

st.set_page_config(page_title="Learning Patterns Dashboard", layout="wide")
st.sidebar.header("User Info")
name     = st.sidebar.text_input("Full Name", "Test User")
gender   = st.sidebar.selectbox("Gender", ["Female","Male","Other"])
country  = st.sidebar.selectbox("Country", ["Singapore","Malaysia","Taiwan"])
dob_text = st.sidebar.text_input("Date of Birth (e.g. 01 January 2010)","01 January 2010")

if st.sidebar.button("Analyze"):
    # Parse DOB → age
    try:
        bd = parser.parse(dob_text, dayfirst=True)
        today = datetime.today()
        age = today.year - bd.year - ((today.month,today.day)<(bd.month,bd.day))
    except:
        st.error("❌ Invalid DOB format.")
        st.stop()

    # Optional: call OpenAI here
    
    # Demo data
    data = {
      "study_time":   {"labels":["<5h","5–10h",">10h"], "values":[35,55,10]},
      "learning_styles": {"labels":["Visual","Auditory","Kinesthetic"], "values":[40,30,30]},
      "math_perf": {"subjects":["Algebra","Geometry"], "local":[75,80], "regional":[70,None], "global":[None,75]},
      "findings": [
        f"55% of {age}-yr-old {gender}s in {country} study 5–10 hrs/week.",
        "Learning methods split evenly.",
        f"{country} {gender}s score 80% in Geometry (vs 75% global)."
      ]
    }

    st.title(f"Learning Patterns for {age}-yr-old {gender}s in {country}")

    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.bar(x=data["study_time"]["labels"], y=data["study_time"]["values"],
                      labels={"x":"Study Time","y":"% Students"})
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.bar(x=data["learning_styles"]["labels"], y=data["learning_styles"]["values"],
                      labels={"x":"Learning Style","y":"% Students"})
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Math Performance")
    perf_df = {
      "subject": data["math_perf"]["subjects"],
      "Local":    data["math_perf"]["local"],
      "Regional": data["math_perf"]["regional"],
      "Global":   data["math_perf"]["global"]
    }
    fig3 = px.bar(perf_df, x="subject", y=["Local","Regional","Global"],
                  barmode="group", labels={"value":"Score (%)","subject":"Subject"})
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### Key Findings")
    for f in data["findings"]:
        st.markdown(f"- {f}")
