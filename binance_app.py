import streamlit as st
import pandas as pd
from binance.client import Client
import plotly.graph_objects as go
import time

# --- IDENTIDAD ÉLITE ---
st.set_page_config(page_title="PERFIL ÉLITE", layout="centered")
st.markdown("""
    <style>
    .stApp { background-color: #0B0E11; color: #FFFFFF; }
    .stTextInput>div>div>input { background-color: #161A1E; color: #00FF88; border: 1px solid #00FF88; }
    div[data-testid="stMetric"] { background: rgba(0, 255, 136, 0.05); border: 1px solid #00FF88; border-radius: 15px; }
    h1 { color: #00FF88 !important; text-align: center; }
    .stButton>button { background-color: #00FF88; color: #0B0E11; font-weight: bold; width: 100%; border-radius: 10px; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ CONTROL ÉLITE")

# --- ENTRADA DE DATOS ---
with st.container():
    api_k = st.text_input("API Key", type="password").strip()
    api_s = st.text_input("Secret Key", type="password").strip()
    par = st.selectbox("Activo", ["BTCUSDT", "ETHUSDT", "SOLUSDT"])
    btn = st.button("SOLTAR INFORMACIÓN COMPLETA")

if btn:
    if api_k and api_s:
        try:
            # 1. SINCRONIZACIÓN PREVIA: Creamos un cliente temporal para obtener la hora
            temp_client = Client(api_k, api_s)
            temp_client.API_URL = 'https://api1.binance.com/api'
            s_time = temp_client.get_server_time()['serverTime']
            
            # 2. CLIENTE DEFINITIVO: Ajustamos el offset manualmente
            client = Client(api_k, api_s)
            client.API_URL = 'https://api1.binance.com/api'
            client.timestamp_offset = s_time - int(time.time() * 1000)
            
            # 3. EXTRACCIÓN DE DATOS (RIGOR L10)
            trades = client.get_my_trades(symbol=par, limit=10, recvWindow=60000)
            df = pd.DataFrame(trades)

            if not df.empty:
                # Convertir datos a números
                df['price'] = pd.to_numeric(df['price'])
                df['qty'] = pd.to_numeric(df['qty'])
                df['quoteQty'] = pd.to_numeric(df['quoteQty'])
                df['commission'] = pd.to_numeric(df['commission'])
                
                # Cálculo de "Ganancia Estimada" (Basada en volumen y tipo)
                # Para un reporte real, Binance no da el PNL directo en trades, se calcula por diferencia
                df['Tipo'] = df['isBuyer'].apply(lambda x: 'COMPRA' if x else 'VENTA')
                
                # DASHBOARD VISUAL
                c1, c2 = st.columns(2)
                c1.metric("VOLUMEN TOTAL (L10)", f"${df['quoteQty'].sum():.2f}")
                c2.metric("COMISIONES PAGADAS", f"{df['commission'].sum():.4f}")

                # Gráfico de Precios
                fig = go.Figure(go.Scatter(y=df['price'], mode='lines+markers', line=dict(color='#00FF88', width=3)))
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250,
                                  xaxis=dict(showgrid=False), yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
                st.plotly_chart(fig, use_container_width=True)
                
                # INFO DETALLADA SIN CAMBIOS
                st.subheader("📋 REPORTE DETALLADO DE OPERACIONES")
                st.dataframe(df[['time', 'Tipo', 'price', 'qty', 'quoteQty', 'commission']], use_container_width=True)
            else:
                st.info("No se encontraron trades recientes para analizar.")
                
        except Exception as e:
            st.error(f"Error Crítico de Sincronización: {e}")
            st.warning("Verifica que tu PC tenga la 'Hora Automática' activada.")
    else:
        st.warning("⚠️ Introduce tus llaves.")
