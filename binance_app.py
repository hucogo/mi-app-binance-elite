import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. CONFIGURACIÓN DE APP MÓVIL ---
st.set_page_config(page_title="CONTROL ÉLITE", page_icon="🛡️", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0B0E11; color: #FFFFFF; }
    .app-card {
        background: #161A1E;
        border: 2px solid #00FF88;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0px 10px 30px rgba(0, 255, 136, 0.1);
    }
    div[data-testid="stMetric"] {
        background: #1C2127;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(0, 255, 136, 0.3);
    }
    .stButton>button {
        background: linear-gradient(135deg, #00FF88 0%, #00cc6e 100%);
        color: #0B0E11;
        font-weight: 800;
        height: 65px;
        border-radius: 15px;
        font-size: 20px;
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATOS DE RIGOR (FUERA DE LA FUNCIÓN PARA EVITAR EL ERROR) ---
precios_lista = [96200, 96350, 96100, 96480, 96600, 96550, 96800, 96720, 96950, 97100]

def generar_datos_app():
    ahora = datetime.now()
    datos = []
    for i in range(10):
        p_actual = precios_lista[i]
        datos.append({
            "Hora": (ahora - timedelta(minutes=(10-i)*15)).strftime("%H:%M"),
            "Op": "BUY" if i % 2 == 0 else "SELL",
            "Precio": f"{p_actual:,.0f}",
            "Profit": f"+{round(1.5 + (i*0.5), 1)}%"
        })
    return pd.DataFrame(datos)

df_app = generar_datos_app()

# --- 3. INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #00FF88;'>🛡️ CONTROL ÉLITE</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.text_input("API KEY", value="PRUEBA_MÓVIL_ACTIVA", disabled=True)
    st.text_input("SECRET KEY", value="••••••••••••", type="password", disabled=True)
    if st.button("SOLTAR INFORMACIÓN"):
        st.balloons()
    st.markdown('</div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    st.metric("GANANCIA L10", "$1,842.20", "+14.5%")
with c2:
    st.metric("VOLUMEN", "$64,250", "AUDITADO")

st.markdown("### 📈 CURVA DE TRADES")
# Aquí usamos precios_lista que ahora sí está definida para el gráfico
fig = go.Figure(go.Scatter(
    x=df_app['Hora'], y=precios_lista,
    mode='lines+markers', line=dict(color='#00FF88', width=5, shape='spline'),
    fill='tozeroy', fillcolor='rgba(0, 255, 136, 0.05)'
))
