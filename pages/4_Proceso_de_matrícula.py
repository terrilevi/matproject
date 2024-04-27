import streamlit as st
import pandas as pd

from login import autenticacion_usuario

def main():
    if autenticacion_usuario():
        st.title("Proceso de matrícula")
        st.subheader("Grafo de los cursos habilitados para el alumno(grafo de Alex)")
        # Check if 'df' exists in session state
        if 'df' not in st.session_state:
            st.error("Primero carga el Plan de Estudios")
        else:
            df = st.session_state['df']
            st.write(df)
    else:
        st.error("Debes iniciar sesión para ver el contenido.")

if __name__ == "__main__":
    main()
