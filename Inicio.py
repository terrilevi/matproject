import streamlit as st
import pandas as pd
import os
from login import autenticacion_usuario

######Esta es la pagina principal(MAIN)##########

####Configuracion de página#######
st.set_page_config(
    page_title="Portal de Matrícula"
        )
##################################


def main():
    if autenticacion_usuario():
        st.title("Datos del estudiante")
        ###Solo son ejemplos, luego haré que lea de frente de la base de datos: bd_alumnos
        st.subheader("Alumno: Alexander")
        st.caption("Ciclo: 5to")




if __name__ == "__main__":
    main()
