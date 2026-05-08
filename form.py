import streamlit as st
from db import get_products, in_orders, delete_product,update_product,add_product


def page_form():
    user = st.session_state.get("user")
    if user["role"] != "Администратор":
        st.error("Только для администратора")
        if st.button("Назад"):
            st.session_state.page = "products"
            st.rerun()
        return
    
    st.set_page_config(page_title="Товар")
    st.title("Редактирование товара" if st.session_state.get("edit") else "Новый товар")
    
    p = None
    if st.session_state.get("edit"):
        p = next((x for x in get_products() if x["article"] == st.session_state.edit), None)
        if not p:
            st.error("Товар не найден")
            if st.button("Назад"):
                st.session_state.page = "products"
                st.rerun()
            return
    
    with st.form("product"):
        c1, c2 = st.columns(2)
        with c1:
            article = st.text_input("Артикул *", value=p["article"] if p else "", disabled=bool(p))
            name = st.text_input("Наименование *", value=p["name"] if p else "")
            category = st.text_input("Категория", value=p.get("category") or "")
            manufacturer = st.text_input("Производитель", value=p.get("manufacturer") or "")
            supplier = st.text_input("Поставщик", value=p.get("supplier") or "")
            unit = st.selectbox("Ед. измерения", ["шт.", "кг", "л", "м", "уп.", "кор."], 
                               index=0 if not p or p["unit"] not in ["шт.", "кг", "л", "м", "уп.", "кор."] else ["шт.", "кг", "л", "м", "уп.", "кор."].index(p["unit"]))
        with c2:
            price = st.number_input("Цена (₽) *", min_value=0.0, step=0.01, value=float(p["price"]) if p else 0.0)
            discount = st.slider("Скидка (%)", 0, 100, int(p.get("discount") or 0))
            stock = st.number_input("На складе", min_value=0, step=1, value=int(p.get("stock_quantity") or 0))
            description = st.text_area("Описание", value=p.get("description") or "", height=80)
        
        cols = st.columns(3)
        save = cols[0].form_submit_button("Сохранить", type="primary")
        cancel = cols[1].form_submit_button("Отмена")
        delete = cols[2].form_submit_button("Удалить") if p else None
    
    if cancel:
        st.session_state.page = "products"
        st.rerun()
    
    if delete and p:
        if in_orders(p["article"]):
            st.warning("Товар в заказах — нельзя удалить")
        else:
            ok, msg = delete_product(p["article"])
            if ok:
                st.success("Удалён")
                st.session_state.page = "products"
                st.rerun()
            else:
                st.error(f"{msg}")
    
    if save:
        if not article or not name:
            st.error("Артикул и наименование обязательны")
        elif price < 0 or stock < 0:
            st.error("Цена и количество не могут быть отрицательными")
        else:
            data = {
                "article": article, "name": name, "unit": unit, "price": price,
                "supplier": supplier, "manufacturer": manufacturer, "category": category,
                "discount": discount, "stock_quantity": stock, "description": description, "photo_url": 'kek'
            }
            
            if p:
                update_product(p["article"], data)
                st.success("Обновлено")
            else:
                ok, msg = add_product(data)
                if ok:
                    st.success("Добавлен")
                else:
                    st.error(f"{msg}")
            
            st.session_state.page = "products"
            st.rerun()
    
    if st.button("Назад к списку"):
        st.session_state.page = "products"
        st.rerun()