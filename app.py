import streamlit as st
import requests

st.set_page_config(page_title="SHL Assessment Recommender")

st.title("🚀 SHL Assessment Recommendation Tool")

st.write("📑 Enter a short description of the role or skills you want to assess.")

API_URL = "https://shl-assessment-recommender-893u.onrender.com/search"

query = st.text_input("Your requirement:")

if st.button("Get Recommendations"):
    if query.strip() == "":
        st.warning("Please enter a requirement.")
    else:
        with st.spinner("Finding best assessments..."):
            response = requests.get(API_URL, params={"query": query})

        if response.status_code != 200:
            st.error("API error. Please try again later.")
        else:
            data = response.json()
            results = data.get("results", [])

            st.subheader("Top matching assessments")

            if not results:
                st.info("No matching assessments found.")
            else:
                for r in results:
                    st.markdown(
                        f"**{r['name']}**  \n"
                        f"Score: {r['score']}  \n"
                        f"[View assessment]({r['url']})"
                    )
