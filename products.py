import streamlit as st
from db import get_suppliers, get_products, in_orders, delete_product


def page_products():
    user = st.session_state.get("user")
    
    st.set_page_config(page_title="Товары", layout="wide")
    
    col1, col2, col3 = st.columns([1, 3, 1])
    with col1:
        st.image("import\Icon.JPG", width=60)
    with col2:
        st.title("Каталог товаров")
    with col3:
        st.write(f"{user['full_name']}")
        if st.button(" Выход"):
            st.session_state.clear()
            st.rerun()
    
    # (менеджер/админ)
    if user["role"] in ("Менеджер", "Администратор"):
        with st.expander("Поиск и фильтры", expanded=True):
            c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
            search = c1.text_input("Поиск", placeholder="название, артикул, описание...")
            suppliers = ["Все поставщики"] + get_suppliers()
            supplier = c2.selectbox("Поставщик", suppliers)
            sort = c3.selectbox("Сортировка по наличию", ["—", "по возрастанию", "по убыванию"])
            sort_map = {"—": "", "по возрастанию": "asc", "по убыванию": "desc"}
            if c4.button("Товар") and user["role"] == "Администратор":
                st.session_state.edit = None
                st.session_state.page = "form"
                st.rerun()
    else:
        search, supplier, sort = "", "", ""
        sort_map = {"": ""}
    
    products = get_products(search, supplier, sort_map.get(sort, ""))
    
    if not products:
        st.info("Товары не найдены")
        if user["role"] == "Администратор" and st.button("Добавить первый товар"):
            st.session_state.edit = None
            st.session_state.page = "form"
            st.rerun()
        return
    
    for p in products:
        with st.container():
            cols = st.columns([1, 3, 2, 1])
            
            with cols[1]:
                st.markdown(f"**{p['name']}**")
                st.caption(f"Артикул: `{p['article']}` | {p.get('category') or '—'}")
                if p.get('description'):
                    st.caption(p['description'][:120] + "…" if len(p['description']) > 120 else p['description'])
                st.caption(f"🏭 {p.get('manufacturer') or '—'} | 📦 {p.get('supplier') or '—'}")
            
            with cols[2]:
                st.markdown(p['price'], unsafe_allow_html=True)
                if p.get('discount'):
                    st.caption(f"Скидка {p['discount']}%")
                stock = p.get('stock_quantity', 0)
                if stock > 0:
                    st.success(f"{stock} {p.get('unit','шт.')}")
                else:
                    st.error(" Нет в наличии")
            
            # (админ)
            with cols[3]:
                if user["role"] == "Администратор":
                    if st.button("✏️", key=f"e_{p['article']}"):
                        st.session_state.edit = p['article']
                        st.session_state.page = "form"
                        st.rerun()
                    if st.button("🗑️", key=f"d_{p['article']}"):
                        if in_orders(p['article']):
                            st.warning("Товар в заказах — нельзя удалить")
                        else:
                            ok, msg = delete_product(p['article'])
                            if ok:
                                st.success("Удалён")
                                st.rerun()
                            else:
                                st.error(f"{msg}")