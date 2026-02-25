import streamlit as st
import pandas as pd
from binance.client import Client
import plotly.graph_objects as go
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="PERFIL ÉLITE LIVE", layout="centered")

# --- DISEÑO VISUAL "PERFIL ÉLITE" ---
st.markdown("""
    <style>
    .stApp { background-color: #0B0E11; color: #FFFFFF; }
    .stTextInput>div>div>input { background-color: #161A1E; color: #00FF88; border: 1px solid #00FF88; }
    div[data-testid="stMetric"] { background: rgba(0, 255, 136, 0.05); border: 1px solid #00FF88; border-radius: 15px; padding: 10px; }
    h1, h2, h3 { color: #00FF88 !important; text-align: center; font-family: 'Inter'; }
    .stButton>button { background-color: #00FF88; color: #0B0E11; font-weight: bold; width: 100%; border-radius: 10px; border: none; height: 3em; }
    .stButton>button:hover { background-color: #00cc6e; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ CONTROL ÉLITE")

# --- INTERFAZ DE ENTRADA ---
with st.container():
    st.markdown("### 🔑 ACCESO API BINANCE")
    col_a, col_b = st.columns(2)
    with col_a:
        api_key = st.text_input("API Key", type="password", placeholder="Pega tu Key")
    with col_b:
        api_secret = st.text_input("Secret Key", type="password", placeholder="Pega tu Secret")
    
    par_busqueda = st.selectbox("Par a analizar (Rigor L10)", ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"])
    conectar = st.button("EXTRAER INFORMACIÓN ÉLITE")

# --- LÓGICA DE CONEXIÓN Y EXTRACCIÓN ---
if conectar:
    if not api_key or not api_secret:
        st.warning("⚠️ Se requieren ambas llaves para iniciar el análisis.")
    else:
        with st.status("Conectando con Binance Global...", expanded=True) as status:
            try:
                # CORRECCIÓN DE UBICACIÓN: Usamos endpoints alternativos que suelen evadir bloqueos de centros de datos
                client = Client(api_key, api_secret)
                client.API_URL = 'https://api1.binance.com/api' # Endpoint alternativo 1
                
                # Test de conexión rápido (obtenemos saldo de la moneda base)
                asset = par_busqueda.replace("USDT", "")
                balance = client.get_asset_balance(asset=asset)
                
                # Extracción de los últimos 10 trades (Rigor L10)
                st.write("Buscando últimos 10 juegos/trades...")
                trades = client.get_my_trades(symbol=par_busqueda, limit=10)
                df = pd.DataFrame(trades)
                
                status.update(label="✅ Conexión Exitosa", state="complete", expanded=False)

                if not df.empty:
                    # PROCESAMIENTO DE DATOS
                    df['price'] = pd.to_numeric(df['price'])
                    df['qty'] = pd.to_numeric(df['qty'])
                    df['quoteQty'] = pd.to_numeric(df['quoteQty']) # Total en dólares
                    df['time'] = pd.to_datetime(df['time'], unit='ms')

                    # DASHBOARD DE RESULTADOS
                    st.markdown("---")
                    st.subheader(f"MÉTRICAS: {par_busqueda}")
                    
                    m1, m2 = st.columns(2)
                    m1.metric("SALDO DISPONIBLE", f"{float(balance['free']):.4f} {asset}")
                    m2.metric("VOLUMEN TOTAL L10", f"${df['quoteQty'].sum():.2f}")

                    # GRÁFICO DINÁMICO
                    st.markdown("### ANÁLISIS DE PRECIO (L10)")
                    fig = go.Figure(go.Scatter(
                        x=df['time'], y=df['price'],
                        mode='lines+markers',
                        line=dict(color='#00FF88', width=3),
                        marker=dict(size=10, color='#FFFFFF', line=dict(width=2, color='#00FF88')),
                        fill='tozeroy',
                        fillcolor='rgba(0, 255, 136, 0.1)'
                    ))
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=0,r=0,t=0,b=0), height=250,
                        xaxis=dict(showgrid=False, font=dict(color="white")),
                        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', font=dict(color="white"))
                    )
                    st.plotly_chart(fig, use_container_width=True)

                    # TABLA DE RIGOR
                    st.subheader("📋 BITÁCORA DETALLADA")
                    df_final = df[['time', 'price', 'qty', 'quoteQty', 'isBuyer']].copy()
                    df_final.columns = ['Fecha', 'Precio', 'Cantidad', 'Total USD', 'Es Compra']
                    st.dataframe(df_final, use_container_width=True)
                else:
                    st.info(f"No se encontraron trades recientes para {par_busqueda}.")

            except Exception as e:
                st.error(f"Error de Binance: {e}")
                st.markdown("""> **Nota Élite:** Si el error de 'Restricted Location' persiste, Binance ha bloqueado totalmente la IP de este servidor en la nube. La solución definitiva es ejecutar este mismo código **localmente** en tu PC para usar tu internet personal.""")

else:
    st.markdown("<br><p style='text-align:center; color:#888;'>Esperando credenciales para soltar la información...</p>", unsafe_allow_html=True)
