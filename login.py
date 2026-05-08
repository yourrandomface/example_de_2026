import streamlit as st
from db import auth_user

def page_login():
    st.title("Система управления товарами")
    

    st.image("import\Icon.ico", width=150)
    
    with st.form("auth"):
        login = st.text_input("Логин")
        pwd = st.text_input("Пароль", type="password")
        col1, col2 = st.columns(2)
        with col1:
            ok = st.form_submit_button("Войти", type="primary")
        with col2:
            guest = st.form_submit_button("Гость")
    
    if ok:
        user = auth_user(login, pwd)
        if user:
            st.session_state.user = dict(user)
            st.session_state.page = "products"
            st.rerun()
        else:
            st.error("Неверный логин или пароль")
    
    if guest:
        st.session_state.user = {"role": "гость", "full_name": "Гость"}
        st.session_state.page = "products"
        st.rerun()