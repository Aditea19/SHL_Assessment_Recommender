import streamlit as st
from retrieval.search import search_assessments

st.set_page_config(page_title="SHL Assessment Recommender")

st.title("🚀 SHL Assessment Recommendation Tool")

st.write(
    "📑Enter a short description of the role or skills you want to assess."
)

query = st.text_input("Your requirement:")

if st.button("Get Recommendations"):
    if query.strip() == "":
        st.warning("Please enter a requirement.")
    else:
        results = search_assessments(query)

        st.subheader("Top matching assessments")
        for r in results:
            st.markdown(
                f"**{r['name']}**  \n"
                f"Score: {r['score']}  \n"
                f"[View assessment]({r['url']})"
            )
