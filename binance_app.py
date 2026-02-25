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
        color: #0B0E11; font-weight: 800; height: 60px; border-radius: 15px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATOS GLOBALES (OBLIGATORIOS PARA EL GRÁFICO) ---
# Definimos los precios aquí afuera para que NUNCA fallen
precios_grafico = [96200, 96350, 96100, 96480, 96600, 96550, 96800, 96720, 96950, 97100]
horas_grafico = [(datetime.now() - timedelta(minutes=(10-i)*15)).strftime("%H:%M") for i in range(10)]

def generar_datos_tabla():
    datos = []
    for i in range(10):
        datos.append({
            "Hora": horas_grafico[i],
            "Op": "BUY" if i % 2 == 0 else "SELL",
            "Precio": f"{precios_grafico[i]:,}",
            "Profit": f"+{round(1.5 + (i*0.5), 1)}%"
        })
    return pd.DataFrame(datos)

df_app = generar_datos_tabla()

# --- 3. INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #00FF88;'>🛡️ CONTROL ÉLITE</h1>", unsafe_allow_html=True)

# Acceso
st.markdown('<div class="app-card">', unsafe_allow_html=True)
st.text_input("API KEY", value="PRUEBA_MÓVIL_ACTIVA", disabled=True)
st.text_input("SECRET KEY", value="••••••••••••", type="password", disabled=True)
st.button("SOLTAR INFORMACIÓN")
st.markdown('</div>', unsafe_allow_html=True)

# Métricas
c1, c2 = st.columns(2)
c1.metric("GANANCIA L10", "$1,842.20", "+14.5%")
c2.metric("VOLUMEN", "$64,250", "AUDITADO")

# --- LA CURVA DE TRADES (CORREGIDA) ---
st.markdown("### 📈 CURVA DE TRADES")

# Creamos el objeto figura explícitamente
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=horas_grafico, 
    y=precios_grafico,
    mode='lines+markers',
    line=dict(color='#00FF88', width=4, shape='spline'),
    marker=dict(size=8, color='#00FF88'),
    fill='tozeroy',
    fillcolor='rgba(0, 255, 136, 0.1)'
))

fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=5, r=5, t=5, b=5),
    height=200,
    xaxis=dict(visible=False),
    yaxis=dict(visible=False, range=[min(precios_grafico)-500, max(precios_grafico)+500])
)

# Renderizado forzado para móvil
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Tabla
st.markdown("### 📋 ÚLTIMOS 10 JUEGOS")
st.dataframe(df_app, use_container_width=True)

st.markdown("---")
st.caption("📱 CONTROL ÉLITE | Rigor L10")
