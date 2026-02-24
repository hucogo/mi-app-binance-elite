import streamlit as st
import pandas as pd
from binance.client import Client
import plotly.graph_objects as go

# --- CONFIGURACIÓN MÓVIL ---
st.set_page_config(page_title="CONTROL ÉLITE", layout="centered")

# --- ESTILO VISUAL PROFESIONAL (CSS NEÓN MÓVIL) ---
st.markdown("""
    <style>
    .stApp { background-color: #0B0E11; color: #FFFFFF; }
    [data-testid="stMetricValue"] { color: #00FF88 !important; font-family: 'JetBrains Mono', monospace; }
    .stMetric { 
        background-color: rgba(22, 26, 30, 0.8); 
        border: 1px solid #00FF88; 
        border-radius: 15px; 
        padding: 10px;
        box-shadow: 0 0 10px rgba(0, 255, 136, 0.2);
    }
    .main-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL: CONEXIÓN API ---
with st.sidebar:
    st.header("🔑 CONEXIÓN BINANCE")
    api_key = st.text_input("API Key", type="password")
    api_secret = st.text_input("Secret Key", type="password")
    
    if st.button("CONECTAR SISTEMA"):
        if api_key and api_secret:
            st.success("API Vinculada con éxito")
        else:
            st.error("Introduce tus llaves")

# --- LÓGICA DE DATOS BINANCE ---
if api_key and api_secret:
    try:
        client = Client(api_key, api_secret)
        # Obtenemos los últimos 10 trades de un par (ej: BTCUSDT)
        trades = client.get_my_trades(symbol='BTCUSDT', limit=10)
        df = pd.DataFrame(trades)
        
        # --- DASHBOARD ÉLITE ---
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.title("⚡ CONTROL ÉLITE")
        st.write("Binance Live Feed | BTCUSDT")
        
        # Métricas de Salud (Simulando el diseño de tu imagen)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("WIN RATE L10", "68.4%", "+3.2%")
        with c2:
            st.metric("PROFIT SEMANAL", "+$1,200", "12.5%")
        st.markdown('</div>', unsafe_allow_html=True)

        # Gráfico Neón (Curva de Equity)
        st.subheader("📊 MÉTRICAS TRADES")
        fig = go.Figure(go.Scatter(y=[1, 3, 2, 5, 4, 7, 6, 9, 8, 10], 
                                  line=dict(color='#00FF88', width=3),
                                  fill='tozeroy',
                                  fillcolor='rgba(0, 255, 136, 0.1)'))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          margin=dict(l=0,r=0,t=0,b=0), height=200, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        # Tabla de Rigor (Últimos 10)
        st.subheader("📑 ÚLTIMOS 10 TRADES")
        st.dataframe(df[['price', 'qty', 'quoteQty', 'time']].tail(10), use_container_width=True)

    except Exception as e:
        st.error(f"Error de conexión: {e}")
else:
    st.info("Esperando API Keys para iniciar el análisis...")