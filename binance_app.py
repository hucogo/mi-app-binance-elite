import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURACIÓN MÓVIL ÉLITE ---
st.set_page_config(page_title="PERFIL ÉLITE", layout="centered")

# URL de tu Google Sheets (Base de datos)
DATA_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRmo-aF0n8t2nhg5Xqv9GrUSl_kbhEMbClivKXhi2BysHmE2B_jZ2mQAFeb6RQQ0WyPM84MrZQTSwn1/pub?output=csv"

# --- DISEÑO VISUAL "PERFIL ÉLITE" (CSS MEJORADO) ---
st.markdown("""
    <style>
    .stApp { background-color: #0B0E11; color: #FFFFFF; }
    /* Tarjetas de Métricas Estilo Imagen */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid #00FF88;
        border-radius: 15px;
        padding: 10px;
    }
    h1, h2, h3 { color: #00FF88 !important; font-family: 'Inter', sans-serif; text-align: center; }
    /* Estilo de la tabla para móvil */
    .stDataFrame { border: 1px solid #00FF88; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CARGA DE DATOS ---
def cargar_datos():
    try:
        df = pd.read_csv(DATA_URL)
        df['Resultado ($)'] = pd.to_numeric(df['Resultado ($)'], errors='coerce')
        return df.tail(10).iloc[::-1]
    except:
        return pd.DataFrame()

df_elite = cargar_datos()

# --- INTERFAZ VISUAL ---
st.title("🛡️ PERFIL ÉLITE")

if not df_elite.empty:
    # Fila de métricas
    c1, c2 = st.columns(2)
    win_rate = (df_elite['Resultado ($)'] > 0).mean() * 100
    profit_total = df_elite['Resultado ($)'].sum()
    
    c1.metric("WIN RATE L10", f"{win_rate:.0f}%")
    c2.metric("PROFIT DIARIO", f"${profit_total:.2f}")

    # GRÁFICO SIN ERRORES
    st.markdown("### RENDIMIENTO")
    fig = go.Figure(go.Scatter(
        y=df_elite['Resultado ($)'].cumsum(), 
        line=dict(color='#00FF88', width=4),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 136, 0.1)'
    ))
    
    # Ajuste del layout (Aquí estaba el error anterior)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0), 
        height=250,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', zeroline=False)
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # ÚLTIMOS TRADES
    st.markdown("### ÚLTIMOS 10 TRADES")
    st.dataframe(df_elite[['Activo', 'Resultado ($)']], use_container_width=True)

else:
    st.warning("⚠️ Sin datos. Revisa tu Google Sheets.")

# --- BARRA LATERAL ---
with st.sidebar:
    st.header("SISTEMA ÉLITE")
    st.write("Estado: **OPERATIVO** 🟢")
    st.write("Disciplina: **DIAMANTE** 💎")
