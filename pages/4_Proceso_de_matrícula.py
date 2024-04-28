import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network

from login import autenticacion_usuario

def draw_graph(df):
    """Draws the graph with the approved courses and courses the user can take, showing direct prerequisite connections."""
    ciclo_actual = int(st.session_state['ciclo_actual'])
    cursos_aprobados = set(st.session_state['cursos_aprobados'])

    df['Ciclo'] = pd.to_numeric(df['Ciclo'], errors='coerce')
    df['Código'] = df['Código'].astype(str).str.strip()
    df['Requisito'] = df['Requisito'].astype(str).str.strip()

    # Create the directed graph
    G = nx.DiGraph()
    for index, row in df.iterrows():
        # Filter courses within 3 cycles ahead of the current one
        if row['Ciclo'] <= ciclo_actual + 3:
            # Add node for the current course if not already present
            if row['Código'] in cursos_aprobados:
                color = 'green'
            elif row['Requisito'] in cursos_aprobados and row['Requisito'] != 'Ninguno':
                color = 'blue'  # Available to take
            else:
                color = 'gray'  # Not available

            G.add_node(row['Código'], title=row['Código'], color=color)

            # Add edges for prerequisite if it's not 'Ninguno'
            if row['Requisito'] != 'Ninguno':
                prereq_color = 'green' if row['Requisito'] in cursos_aprobados else 'gray'
                G.add_node(row['Requisito'], title=row['Requisito'], color=prereq_color)
                G.add_edge(row['Requisito'], row['Código'])

    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
    # Add nodes and edges to the network graph
    for node, node_attrs in G.nodes(data=True):
        net.add_node(node, title=node, color=node_attrs['color'])
    for edge in G.edges():
        net.add_edge(edge[0], edge[1])

    # Save and display the graph
    net.save_graph("graph.html")
    HtmlFile = open("graph.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    st.components.v1.html(source_code, height=800)


def main():
    if autenticacion_usuario():
        st.title("Proceso de matrícula")
        st.subheader("Grafo de los cursos habilitados para el alumno(grafo de Alex)")
        if 'df' in st.session_state:
            df = st.session_state['df']
            st.write(df)
            st.write(f"Hola, {st.session_state['nombre']}!")
            st.write(f"Ciclo: {st.session_state['ciclo_actual']}")
            st.write(f"Cursos: {st.session_state['cursos_aprobados']}")
            draw_graph(df)
        else:
            st.error("Primero carga el Plan de Estudios")
    else:
        st.error("Debes iniciar sesión para ver el contenido.")

if __name__ == "__main__":
    main()


