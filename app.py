"""
App entrypoint.

Author: Yakir Havin
"""

import streamlit as st


st.logo("assets/contourcfo_logo.png")


def login():
    st.set_page_config(
        page_title="Home | Executive Portal Demo",
        layout="centered"
    )
    st.image("assets/contourcfo_logo.png", width=175)
    st.divider(width=100)
    st.title(":material/dashboard: Executive Portal Demo")

    if "logged_in" not in st.session_state:
        password_form_container = st.empty()

        password_form = password_form_container.form(key="password-form", clear_on_submit=True, border=False)
        password = password_form.text_input(
            label="Password",
            placeholder="Enter password to access this demo"
        )

        submitted = password_form.form_submit_button("Submit")
        if submitted:
            try:
                int(password)
            except ValueError:
                st.error("Incorrect password. Please try again.")
                st.stop()

            if int(password) % 7 == 0:  # Password is any multiple of 7
                st.session_state["logged_in"] = True
                st.success("Logged in successfully.")
                password_form_container.empty()
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        st.text("Your home for company reports and data insights")


login_page = st.Page(
    page=login,
    title="Home",
    icon=":material/home:"
)
executive_summary_page = st.Page(
    page="executive_summary.py",
    title="Executive summary",
    url_path="executive-summary",
    icon=":material/health_metrics:"
)
performance_explorer_page = st.Page(
    page="performance_explorer.py",
    title="Performance explorer",
    url_path="performance-explorer",
    icon=":material/explore:"
)
financial_statements_page = st.Page(
    page="financial_statements.py",
    title="Financial statements",
    url_path="financial-statements",
    icon=":material/article:"
)

if st.session_state.get("logged_in", False):
    navigation = [
        login_page, 
        executive_summary_page,
        performance_explorer_page,
        financial_statements_page
    ]
    
    pg = st.navigation(navigation, expanded=True)
else:
    pg = st.navigation([login_page])

pg.run()