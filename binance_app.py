import streamlit as st
import pandas as pd
from binance.client import Client
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE PÁGINA MÓVIL ---
st.set_page_config(page_title="BINANCE ÉLITE", layout="centered")

# --- ESTILO VISUAL "PERFIL ÉLITE" ---
st.markdown("""
    <style>
    .stApp { background-color: #0B0E11; color: #FFFFFF; }
    .stTextInput>div>div>input {
        background-color: #161A1E; color: #00FF88; border: 1px solid #00FF88;
    }
    div[data-testid="stMetric"] {
        background: rgba(0, 255, 136, 0.05); border: 1px solid #00FF88; border-radius: 15px;
    }
    h1, h2 { color: #00FF88 !important; text-align: center; }
    .stButton>button {
        background-color: #00FF88; color: #0B0E11; font-weight: bold; width: 100%; border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ CONTROL ÉLITE")

# --- APARTADO PARA COLOCAR LAS APIS ---
with st.expander("🔑 CONFIGURAR LLAVES DE BINANCE", expanded=True):
    api_key = st.text_input("Ingresa tu API Key", type="password")
    api_secret = st.text_input("Ingresa tu Secret Key", type="password")
    boton_conectar = st.button("CONECTAR Y EXTRAER INFO")

# --- LÓGICA DE EXTRACCIÓN ---
if boton_conectar or (api_key and api_secret):
    if not api_key or not api_secret:
        st.error("Por favor, introduce ambas llaves.")
    else:
        try:
            # Conexión Real con Binance
            client = Client(api_key, api_secret)
            
            # 1. Obtener Saldo de Cuenta
            info = client.get_account()
            balances = [d for d in info['balances'] if float(d['free']) > 0 or float(d['locked']) > 0]
            
            # 2. Obtener últimos 10 trades (Rigor L10)
            # Por defecto busca BTCUSDT, puedes cambiarlo o hacerlo dinámico
            trades = client.get_my_trades(symbol='BTCUSDT', limit=10)
            df = pd.DataFrame(trades)

            if not df.empty:
                # Procesamiento de Datos
                df['price'] = pd.to_numeric(df['price'])
                df['qty'] = pd.to_numeric(df['qty'])
                df['quoteQty'] = pd.to_numeric(df['quoteQty']) # Volumen en USD

                # MÉTRICAS EN PANTALLA
                st.subheader("MÉTRICAS DE SALUD")
                c1, c2 = st.columns(2)
                c1.metric("TOTAL VOLUMEN (L10)", f"${df['quoteQty'].sum():.2f}")
                c2.metric("TRADES ACTIVOS", len(df))

                # GRÁFICO DE OPERACIONES
                st.subheader("📊 HISTORIAL DE PRECIOS")
                fig = go.Figure(go.Scatter(y=df['price'], line=dict(color='#00FF88', width=3), fill='tozeroy'))
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=200,
                                  xaxis=dict(showgrid=False), yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
                st.plotly_chart(fig, use_container_width=True)

                # TABLA DETALLADA (TODA LA INFO)
                st.subheader("📋 DETALLE DE OPERACIONES")
                st.dataframe(df[['price', 'qty', 'quoteQty', 'time']], use_container_width=True)
            else:
                st.warning("Conectado, pero no se encontraron trades recientes en BTCUSDT.")

        except Exception as e:
            # Manejo de error de IP o Llaves
            st.error(f"Error de Binance: {e}")
            st.info("Nota: Si el error es 'Restricted Location', es por el bloqueo de IP del servidor.")

else:
    st.info("Introduce tus credenciales arriba para visualizar el Perfil Élite.")
