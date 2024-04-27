import streamlit as st
import pandas as pd

from login import autenticacion_usuario

def main():
    if autenticacion_usuario():
        st.title("Plan de estudios")
        st.subheader("Grafo del plan de estudios de la carrera Ing. Informática(Grafo Magno)")
        # Chequea primero si hay un df activo, si no, te sale un mensaje y no un error
        if 'df' not in st.session_state:
            st.error("Primero carga el Plan de Estudios")
        else:
            df = st.session_state['df']
            st.write(df)
    else:
        st.error("Debes iniciar sesión para ver el contenido.")

if __name__ == "__main__":
    main()
