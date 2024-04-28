import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network

from login import autenticacion_usuario

def draw_graph(df, user_info):
    ciclo_actual = int(user_info['ciclo_actual'])
    cursos_aprobados = set(user_info['cursos_aprobados'])

    # This part of the code assumes 'Ciclo', 'Código', and 'Requisito' are column names in your DataFrame
    # Ensure these match the actual column names in your DataFrame
    df['Ciclo'] = pd.to_numeric(df['Ciclo'], errors='coerce')
    df['Código'] = df['Código'].astype(str).str.strip()
    df['Requisito'] = df['Requisito'].astype(str).str.strip()

    G = nx.DiGraph()
    for index, row in df.iterrows():
        G.add_node(row['Código'], title=row['Código'], color='green' if row['Código'] in cursos_aprobados else 'gray')
        if row['Requisito'] != 'Ninguno':
            G.add_node(row['Requisito'], title=row['Requisito'], color='green' if row['Requisito'] in cursos_aprobados else 'gray')
            G.add_edge(row['Requisito'], row['Código'])
            if row['Requisito'] in cursos_aprobados and row['Código'] not in cursos_aprobados:
                G.nodes[row['Código']]['color'] = 'blue'
                
    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    for node, node_attrs in G.nodes(data=True):
        net.add_node(node, title=node, color=node_attrs['color'])
    for edge in G.edges():
        net.add_edge(edge[0], edge[1])

    # Save the graph to an HTML file
    net.save_graph("graph.html")

    # Read the HTML file content and display it using Streamlit
    HtmlFile = open("graph.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()  # Read the HTML file
    st.components.v1.html(source_code, height=800)  # Render HTML in Streamlit


def main():
    if autenticacion_usuario():
        st.title("Proceso de matrícula")
        st.subheader("Grafo de los cursos habilitados para el alumno")
        if 'df' not in st.session_state:
            st.error("Primero carga el Plan de Estudios")
        else:
            df = st.session_state['df']
            user_info = {
                'ciclo_actual': st.session_state['ciclo_actual'],
                'cursos_aprobados': st.session_state['cursos_aprobados']
            }
            draw_graph(df, user_info)
            st.write(f"Hola, {st.session_state['nombre']}!")
            st.write(f"Ciclo: {st.session_state['ciclo_actual']}")
            st.write(f"Cursos: {st.session_state['cursos_aprobados']}")
    else:
        st.error("Debes iniciar sesión para ver el contenido.")

if __name__ == "__main__":
    main()


