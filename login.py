import streamlit as st
import pandas as pd
import os

#Base de datos de alumno
file_path = os.path.join(os.path.dirname(__file__), 'bd_alumnos.csv')
df = pd.read_csv(file_path)
########################



##############Sistema de Login##########################
###################Falta mejorar el login###############
def entrada_credencial():
    # Get the credentials provided by the user
    user_input = st.session_state["user"].strip()
    passwd_input = st.session_state["passwd"].strip()

    if st.session_state["validar"]:
        if any((df['userid'] == user_input) & (df['password'] == passwd_input)):
            st.session_state["autenticacion"] = True
        else:
            st.session_state["autenticacion"] = False
            st.error("Contraseña/Usuario invalido")

def autenticacion_usuario():
    if "autenticacion" not in st.session_state:
        st.markdown("<h1 style='text-align: center;'>Iniciar Sesión 👋</h1>", unsafe_allow_html=True)
        st.text_input(label= "Usuario: ", value="", key="user", on_change=entrada_credencial)
        st.text_input(label= "Contraseña: ", value="", key="passwd", type="password", on_change=entrada_credencial)
        # Agregamos un botón para validar las credenciales
        validar = st.button("Iniciar Sesión")
        if validar:
            st.session_state["validar"] = True
            entrada_credencial()
        else:
            st.session_state["validar"] = False
        return False
    else:
        if st.session_state["autenticacion"]:
            return True
        else:
            st.markdown("<h1 style='text-align: center;'>Iniciar Sesión 👋</h1>", unsafe_allow_html=True)
            st.text_input(label= "Usuario: ", value="", key="user", on_change=entrada_credencial)
            st.text_input(label= "Contraseña: ", value="", key="passwd", type="password", on_change=entrada_credencial)
            validar = st.button("Iniciar Sesión")
            if validar:
                st.session_state["validar"] = True
                entrada_credencial()
            else:
                st.session_state["validar"] = False
            return False
##############Sistema de Login##########################