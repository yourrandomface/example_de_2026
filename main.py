import streamlit as st
from login import page_login
from products import page_products
from form import page_form



def main():
    
    if "page" not in st.session_state:
        st.session_state.page = "login"
    
    if st.session_state.page == "login":
        page_login()
    elif st.session_state.page == "products":
        page_products()
    elif st.session_state.page == "form":
        page_form()
    else:
        st.session_state.page = "login"
        st.rerun()

if __name__ == "__main__":
    main()