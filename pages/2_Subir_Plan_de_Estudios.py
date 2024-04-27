import streamlit as st
import pandas as pd

from login import autenticacion_usuario


def main():
    if autenticacion_usuario():
        st.title("Plan de estudios")
        upload_file = st.file_uploader('Subir el plan de estudios correspondiente a tu carrera')
        if upload_file is not None:
            df = pd.read_csv(upload_file)
            st.session_state['df']= df
    else:
        st.error("Debes iniciar sesión para ver el contenido.")


    



if __name__ == "__main__":
    main()
