import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE APP MÓVIL ---
st.set_page_config(
    page_title="CONTROL ÉLITE",
    page_icon="🛡️",
    layout="centered"
)

# Estilos CSS específicos para interfaz táctil (No se cambia nada de la info)
st.markdown("""
    <style>
    .stApp { background-color: #0B0E11; color: #FFFFFF; }
    
    /* Bloque de conexión estilo Tarjeta App */
    .app-card {
        background: #161A1E;
        border: 2px solid #00FF88;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0px 10px 30px rgba(0, 255, 136, 0.1);
    }
    
    /* Métricas con Rigor L10 */
    div[data-testid="stMetric"] {
        background: #1C2127;
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(0, 255, 136, 0.3);
    }
    
    /* Botón de acción táctil */
    .stButton>button {
        background: linear-gradient(135deg, #00FF88 0%, #00cc6e 100%);
        color: #0B0E11;
        font-weight: 800;
        height: 65px;
        border-radius: 15px;
        font-size: 20px;
        border: none;
    }
    
    /* Tabla estilo Mobile */
    .stDataFrame {
        border: 1px solid #00FF88;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- GENERACIÓN DE DATOS (RIGOR L10) ---
def generar_datos_app():
    ahora = datetime.now()
    # Datos simulados siguiendo el promedio por partido
    precios = [96200, 96350, 96100, 96480, 96600, 96550, 96800, 96720, 96950, 97100]
    datos = []
    for i in range(10):
        p_actual = precios[i]
        datos.append({
            "Hora": (ahora - timedelta(minutes=(10-i)*15)).strftime("%H:%M"),
            "Op": "BUY" if i % 2 == 0 else "SELL",
            "Precio": f"{p_actual:,.0f}",
            "Profit": f"+{round(1.5 + (i*0.5), 1)}%"
        })
    return pd.DataFrame(datos)

df_app = generar_datos_app()

# --- INTERFAZ ---
st.markdown("<h1 style='text-align: center; color: #00FF88;'>🛡️ CONTROL ÉLITE</h1>", unsafe_allow_html=True)

# Sección de Acceso
st.markdown('<div class="app-card">', unsafe_allow_html=True)
st.text_input("API KEY", value="PRUEBA_MÓVIL_ACTIVA", disabled=True)
st.text_input("SECRET KEY", value="••••••••••••", type="password", disabled=True)
if st.button("SOLTAR INFORMACIÓN"):
    st.balloons() # Efecto visual de éxito
st.markdown('</div>', unsafe_allow_html=True)

# Métricas de Rigor
c1, c2 = st.columns(2)
with c1:
    st.metric("GANANCIA L10", "$1,842.20", "+14.5%")
with c2:
    st.metric("VOLUMEN", "$64,250", "AUDITADO")

# Gráfico de Curva (Visible en App)
st.markdown("### 📈 CURVA DE TRADES")
fig = go.Figure(go.Scatter(
    x=df_app['Hora'], y=precios,
    mode='lines+markers', line=dict(color='#00FF88', width=5, shape='spline'),
    fill='tozeroy', fillcolor='rgba(0, 255, 136, 0.05)'
))
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, t=0, b=0), height=180,
    xaxis={"visible": False}, yaxis={"visible": False}
)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Tabla Detallada (Rigor L10)
st.markdown("### 📋 ÚLTIMOS 10 JUEGOS")
st.dataframe(df_app, use_container_width=True)

st.markdown("---")
st.caption("📱 CONTROL ÉLITE v1.0 | Rigor L10 Activo")
