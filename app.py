# Para trabalhar com Streamlit e folium
import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium
import streamlit as st
import plotly.graph_objects as go
from shapely.geometry import Polygon, LineString

# Definir a área agrícola
area = Polygon([(0, 0), (10, 0), (10, 5), (0, 5)])

# Layout com colunas
col1, col2 = st.columns(2)

with col1:
    st.write("Escolha o espaçamento entre as linhas:")
    spacing = st.slider("Espaçamento entre linhas (m)", 0.1, 2.0, 1.0)

with col2:
    st.write("Visualização da área agrícola:")
    # Exiba a visualização aqui

# Gerar as linhas de plantio
min_x, min_y, max_x, max_y = area.bounds
linhas = []
y = min_y
while y <= max_y:
    linha = LineString([(min_x, y), (max_x, y)])
    intersecao = linha.intersection(area)
    if not intersecao.is_empty:
        if intersecao.geom_type == 'MultiLineString':
            linhas.extend(intersecao.geoms)
        else:
            linhas.append(intersecao)
    y += spacing

# Gráfico interativo com plotly
fig = go.Figure()

# Adicionando a área agrícola
fig.add_trace(go.Scatter(
    x=list(area.exterior.xy[0]),
    y=list(area.exterior.xy[1]),
    fill="toself",
    fillcolor="blue",
    line_color="gray",
    name="Área Agrícola"
))

# Adicionando as linhas de plantio
for linha in linhas:
    fig.add_trace(go.Scatter(
        x=list(linha.xy[0]),
        y=list(linha.xy[1]),
        mode='lines',
        line=dict(color='blue'),
        name="Linha de Plantio"
    ))

# Ajuste da aparência
fig.update_layout(
    title="Linhas de Plantio",
    xaxis_title="Longitude",
    yaxis_title="Latitude",
    template="plotly_dark",
    showlegend=True
)

st.plotly_chart(fig)
