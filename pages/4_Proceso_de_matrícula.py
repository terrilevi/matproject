import streamlit as st
import pandas as pd
from pyvis.network import Network

def draw_graph():
    df = st.session_state['df']
    ciclo_actual = int(st.session_state['ciclo_actual'])
    cursos_aprobados = set(st.session_state.get('cursos_aprobados', []))

    df['Ciclo'] = pd.to_numeric(df['Ciclo'], errors='coerce')
    df['Código'] = df['Código'].astype(str).str.strip()
    df['Requisito'] = df['Requisito'].astype(str).str.strip()

    df_filtrado = df[df['Ciclo'] <= ciclo_actual + 3]

    net = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")

    # Create nodes and edges directly in PyVis with color logic
    for index, row in df_filtrado.iterrows():
        code_color = 'green' if row['Código'] in cursos_aprobados else 'gray'
        net.add_node(row['Código'], title=row['Código'], color=code_color)

        if row['Requisito'] != 'Ninguno':
            req_color = 'green' if row['Requisito'] in cursos_aprobados else 'gray'
            net.add_node(row['Requisito'], title=row['Requisito'], color=req_color)
            net.add_edge(row['Requisito'], row['Código'])

            # Update color based on complex condition
            if row['Requisito'] in cursos_aprobados and row['Código'] not in cursos_aprobados:
                net.get_node(row['Código']).update(color='blue')

    net.show("graph.html")
    HtmlFile = open("graph.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read()
    st.components.v1.html(source_code, height=800)

def main():
    if autenticacion_usuario():
        st.title("Proceso de matrícula")
        st.subheader("Grafo de los cursos habilitados para el alumno")
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

