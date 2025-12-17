import streamlit as st
import pandas as pd
from datetime import datetime

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="Inteligência em YouTube Shorts",
    page_icon="🎬",
    layout="wide"
)

# =========================
# CARREGAR DADOS
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("ranking_shorts.csv")
    return df

df = load_data()

# =========================
# HEADER
# =========================
st.title("🎬 Inteligência em YouTube Shorts")
st.caption("Canal: **Cláudio Dantas** | Análise automática de potencial para Shorts")

st.markdown(
    f"""
    **Última atualização:** {datetime.now().strftime('%d/%m/%Y %H:%M')}  
    **Vídeos analisados:** {len(df)}
    """
)

st.divider()

# =========================
# KPIs
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Views médias",
        f"{int(df.views.mean()):,}".replace(",", ".")
    )

with col2:
    st.metric(
        "Engajamento / 1000 views",
        f"{df.engajamento_por_1000_views.mean():.2f}"
    )

with col3:
    st.metric(
        "Melhor Short Score",
        f"{df.short_score.max():.2f}"
    )

with col4:
    best = df.iloc[0]
    st.metric(
        "Melhor Vídeo",
        best.title[:30] + "..."
    )

st.divider()

# =========================
# CONTROLE DE PRIORIZAÇÃO
# =========================
st.subheader("Priorização para Shorts")

top_n = st.slider(
    "Quantos vídeos priorizar?",
    min_value=1,
    max_value=len(df),
    value=5
)

priority_df = df.head(top_n)

st.info(
    "Esses são os vídeos que **devem virar Shorts primeiro**, "
    "com base em engajamento relativo e tração pública."
)

# =========================
# TABELA RANKING
# =========================
st.subheader("Ranking de vídeos por potencial de Shorts")

table_df = priority_df.copy()
table_df["YouTube"] = table_df.video_id.apply(
    lambda x: f"https://www.youtube.com/watch?v={x}"
)

st.dataframe(
    table_df[[
        "title",
        "views",
        "engajamento_por_1000_views",
        "short_score",
        "YouTube"
    ]],
    use_container_width=True,
    column_config={
        "title": "Título",
        "views": st.column_config.NumberColumn("Views", format="%d"),
        "engajamento_por_1000_views": st.column_config.NumberColumn(
            "Engajamento / 1000 views",
            format="%.2f"
        ),
        "short_score": st.column_config.ProgressColumn(
            "Short Score",
            min_value=0,
            max_value=df.short_score.max()
        ),
        "YouTube": st.column_config.LinkColumn("Abrir vídeo")
    }
)

st.divider()

# =========================
# DESTAQUE TOP 3
# =========================
st.subheader("Top 3 vídeos para cortar agora")

cols = st.columns(3)

for i, col in enumerate(cols):
    if i < len(df):
        v = df.iloc[i]
        with col:
            st.markdown(f"### #{i+1}")
            st.markdown(f"**{v.title}**")
            st.markdown(f"- Views: {v.views:,}".replace(",", "."))
            st.markdown(
                f"- Engajamento/1000: {v.engajamento_por_1000_views:.2f}"
            )
            st.markdown(f"- Short Score: **{v.short_score:.2f}**")
            st.link_button(
                "Abrir no YouTube",
                f"https://www.youtube.com/watch?v={v.video_id}"
            )

st.divider()

# =========================
# FOOTER
# =========================
st.caption(
    "Pipeline automático de análise e geração de Shorts • "
    "Protótipo por Carlos Becker"
)
