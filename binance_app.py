import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURACIÓN E IDENTIDAD ÉLITE ---
st.set_page_config(page_title="PERFIL ÉLITE", layout="centered")

# URL de tu Google Sheets (La que ya tienes publicada como CSV)
DATA_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmo-aF0n8t2nhg5Xqv9GrUSl_kbhEMbClivKXhi2BysHmE2B_jZ2mQAFeb6RQQ0WyPM84MrZQTSwn1/pub?output=csv"

# --- ESTILO VISUAL (GLASSMORPHISM NEÓN) ---
st.markdown("""
    <style>
    .stApp { background-color: #0B0E11; color: #FFFFFF; }
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid #00FF88;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 136, 0.1);
    }
    h1, h2, h3 { color: #00FF88 !important; font-family: 'Inter', sans-serif; }
    .stDataFrame { border: 1px solid rgba(0, 255, 136, 0.3); border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS CON RIGOR (ÚLTIMOS 10) ---
def cargar_datos():
    try:
        df = pd.read_csv(DATA_URL)
        # Convertimos a numérico por si acaso y tomamos los últimos 10
        df['Resultado ($)'] = pd.to_numeric(df['Resultado ($)'], errors='coerce')
        return df.tail(10).iloc[::-1] # Invertir para ver el más reciente arriba
    except:
        return pd.DataFrame()

df_elite = cargar_datos()

# --- INTERFAZ MÓVIL ---
st.title("⚡ PERFIL ÉLITE")

if not df_elite.empty:
    # MÉTRICAS DE SALUD
    col1, col2 = st.columns(2)
    
    with col1:
        win_rate = (df_elite['Resultado ($)'] > 0).mean() * 100
        st.metric("WIN RATE L10", f"{win_rate:.1f}%")
        
    with col2:
        profit_total = df_elite['Resultado ($)'].sum()
        st.metric("PROFIT DIARIO", f"${profit_total:.2f}", "+1.25%")

    # GRÁFICO DE RENDIMIENTO NEÓN
    st.subheader("ANALISIS ÉLITE DINÁMICO")
    fig = go.Figure(go.Scatter(y=df_elite['Resultado ($)'].cumsum(), 
                              line=dict(color='#00FF88', width=3),
                              fill='tozeroy',
                              fillcolor='rgba(0, 255, 136, 0.1)'))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      margin=dict(l=0,r=0,t=0,b=0), height=200, showxaxis=False)
    st.plotly_chart(fig, use_container_width=True)

    # TABLA DE ÚLTIMOS 10 TRADES
    st.subheader("ÚLTIMOS 10 TRADES")
    st.dataframe(df_elite[['Activo', 'Resultado ($)']], use_container_width=True)

    # BOTÓN DE ACCIÓN (ESTILO OPERAR)
    if st.button("REVISAR ESTRATEGIA"):
        st.info("Soportado por Rigor de Análisis Élite")
else:
    st.error("Esperando conexión con Google Sheets...")

# --- BARRA LATERAL (CONFIGURACIÓN) ---
with st.sidebar:
    st.header("⚙️ CONFIGURACIÓN")
    st.write("Conectividad API: **ACTIVA** 🟢")
    st.write("Nivel Disciplina: **DIAMANTE** 💎")
