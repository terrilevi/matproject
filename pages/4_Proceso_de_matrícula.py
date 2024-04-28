import streamlit as st
import pandas as pd
from pyvis.network import Network
import networkx as nx
from login import autenticacion_usuario

def draw_graph():
    df = st.session_state['df']
    ciclo_actual = int(st.session_state['ciclo_actual'])
    cursos_aprobados = set(st.session_state.get('cursos_aprobados', []))  # Use get with a default empty list

    df['Ciclo'] = pd.to_numeric(df['Ciclo'], errors='coerce')
    df['Código'] = df['Código'].astype(str).str.strip()
    df['Requisito'] = df['Requisito'].astype(str).str.strip()

    df_filtrado = df[df['Ciclo'] <= ciclo_actual + 3]

    G = nx.DiGraph()
    for index, row in df_filtrado.iterrows():
        if row['Código'] not in G.nodes():
            G.add_node(row['Código'], title=row['Código'], color='green' if row['Código'] in cursos_aprobados else 'gray')
        if row['Requisito'] != 'Ninguno':
            if row['Requisito'] not in G.nodes():
                G.add_node(row['Requisito'], title=row['Requisito'], color='green' if row['Requisito'] in cursos_aprobados else 'gray')
            G.add_edge(row['Requisito'], row['Código'])
            if row['Requisito'] in cursos_aprobados and row['Código'] not in cursos_aprobados:
                G.nodes[row['Código']]['color'] = 'blue'

    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    for node, node_attrs in G.nodes(data=True):
        net.add_node(node, title=node, color=node_attrs['color'])
    for edge in G.edges():
        net.add_edge(edge[0], edge[1])

    net.save_graph("graph.html")
    HtmlFile = open("graph.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    st.components.v1.html(source_code, height=800)

def main():
    if autenticacion_usuario():
        st.title("Proceso de matrícula")
        st.subheader("Grafo de los cursos habilitados para el alumno (grafo de Alex)")
        
        # Initialize session state for cursos_aprobados if not present
        if 'cursos_aprobados' not in st.session_state:
            st.session_state['cursos_aprobados'] = []

        if 'df' not in st.session_state:
            st.error("Primero carga el Plan de Estudios")
        else:
            st.write(f"Cursos aprobados: {st.session_state['cursos_aprobados']}")
            st.write(f"Ciclo actual: {st.session_state['ciclo_actual']}")
            draw_graph() 
    else:
        st.error("Debes iniciar sesión para ver el contenido.")

if __name__ == "__main__":
    main()

