import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE APP MÓVIL ---
st.set_page_config(page_title="CONTROL ÉLITE", layout="centered")

# Estilos CSS específicos para interfaz táctil
st.markdown("""
    <style>
    /* Fondo oscuro profundo */
    .stApp { background-color: #0B0E11; color: #FFFFFF; }
    
    /* Bloque de conexión optimizado para dedo */
    .app-card {
        background: rgba(22, 26, 30, 0.95);
        border: 2px solid #00FF88;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0px 5px 15px rgba(0,0,0,0.5);
    }
    
    /* Métricas en formato App (Grandes y claras) */
    div[data-testid="stMetric"] {
        background: #161A1E;
        border-left: 4px solid #00FF88;
        border-radius: 8px;
        padding: 12px;
    }
    
    /* Botón de acción principal (Estilo App) */
    .stButton>button {
        background: #00FF88;
        color: #0B0E11;
        font-weight: 900;
        height: 60px;
        border-radius: 12px;
        font-size: 18px;
        text-transform: uppercase;
        border: none;
        box-shadow: 0px 4px 10px rgba(0, 255, 136, 0.3);
    }
    
    /* Ajuste de fuentes para pantallas pequeñas */
    h1 { font-size: 28px !important; text-align: center; color: #00FF88 !important; }
    h3 { font-size: 18px !important; color: #00FF88 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- GENERACIÓN DE DATOS SIMULADOS (RIGOR L10) ---
def generar_datos_app():
    ahora = datetime.now()
    precios = [96200, 96350, 96100, 96480, 96600, 96550, 96800, 96720, 96950, 97100]
    datos = []
    for i in range(10):
        p_actual = precios[i]
        datos.append({
            "Hora": (ahora - timedelta(minutes=(10-i)*15)).strftime("%H:%M"),
            "Tipo": "BUY" if i % 2 == 0 else "SELL",
            "Precio": f"{p_actual:,.0f}",
            "Profit": f"+{round(1.2 + i, 1)}%"
        })
    return pd.DataFrame(datos)

df_app = generar_datos_app()

# --- INTERFAZ DE LA APP ---
st.markdown("<h1>🛡️ CONTROL ÉLITE</h1>", unsafe_allow_html=True)

# Contenedor de Acceso
st.markdown('<div class="app-card">', unsafe_allow_html=True)
st.text_input("API KEY", value="PRUEBA_SISTEMA_ACTIVA", disabled=True)
st.text_input("SECRET KEY", value="••••••••••••", type="password", disabled=True)
if st.button("SOLTAR INFORMACIÓN"):
    st.toast("Actualizando datos de mercado...")
st.markdown('</div>', unsafe_allow_html=True)

# Resumen Rápido (Métricas)
col1, col2 = st.columns(2)
with col1:
    st.metric("GANANCIA L10", "$1,842", "+12.5%")
with col2:
    st.metric("VOLUMEN", "$64K", "ESTABLE")

# Gráfico Táctil
st.markdown("### 📈 CURVA DE OPERACIONES")
fig = go.Figure(go.Scatter(
    x=df_app['Hora'], y=precios,
    mode='lines+markers', line=dict(color='#00FF88', width=4, shape='spline'),
    marker=dict(size=8, color='#00FF88'),
    fill='tozeroy', fillcolor='rgba(0, 255, 136, 0.05)'
))
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, t=10, b=0), height=200,
    xaxis={"visible": False}, yaxis={"visible": False}
)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Historial L10 (Sin cambios en la info)
st.markdown("### 📋 ÚLTIMOS 10 JUEGOS")
st.dataframe(df_app, use_container_width=True)

st.markdown("---")
st.caption("📱 Perfil Élite v1.0 - Protocolo Rigor L10 Activo")
