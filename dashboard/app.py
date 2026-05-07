import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Университетская аналитика", layout="wide")
st.title("Университетская аналитика")

CUBE_API = "http://localhost:4000/cubejs-api/v1/load"

def run_query(query):
    response = requests.post(CUBE_API, json={"query": query})
    data = response.json()
    if "data" in data:
        df = pd.DataFrame(data["data"])
        return df
    st.error(f"Ошибка: {data.get('error', 'Неизвестная ошибка')}")
    return None

# Вкладки
tab1, tab2 = st.tabs(["Загрузка кампуса", "Успеваемость"])

with tab1:
    st.header("Загрузка корпусов (реальное время)")
    
    if st.button("Обновить данные"):
        st.rerun()
    
    query = {
        "measures": ["PeopleCount.total_people"],
        "dimensions": ["PeopleCount.building_id"],
        "order": {"PeopleCount.building_id": "asc"}
    }
    df = run_query(query)
    
    if df is not None:
        df.columns = ["Корпус", "Количество людей"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df, use_container_width=True)
        with col2:
            fig = px.bar(df, x="Корпус", y="Количество людей", 
                         title="Людей в корпусе", color="Корпус")
            st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Успеваемость студентов")
    
    query2 = {
        "measures": ["StudentFeatures.count", "StudentFeatures.avg_score"],
        "dimensions": ["StudentFeatures.performance_level"],
        "order": {"StudentFeatures.performance_level": "asc"}
    }
    df2 = run_query(query2)
    
    if df2 is not None:
        df2.columns = ["Уровень", "Студентов", "Средний балл"]
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.pie(df2, names="Уровень", values="Студентов",
                         title="Распределение по успеваемости")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.bar(df2, x="Уровень", y="Средний балл",
                         title="Средний балл по уровням", color="Уровень")
            st.plotly_chart(fig, use_container_width=True)
