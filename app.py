import streamlit as st
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, LineString
import numpy as np

st.set_page_config(layout="centered")
st.title("Gerador de Linhas de Plantio")

area = Polygon([(0, 0), (10, 0), (10, 5), (0, 5)])
espacamento = st.slider("Espaçamento entre linhas (m)", 0.1, 2.0, 1.0, step=0.1)

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
    y += espacamento

fig, ax = plt.subplots()
x, y = area.exterior.xy
ax.plot(x, y, color='green', label='Área Agrícola')

for linha in linhas:
    x, y = linha.xy
    ax.plot(x, y, color='blue')

ax.set_title("Linhas de Plantio")
ax.set_aspect('equal')
ax.grid(True)
st.pyplot(fig)
