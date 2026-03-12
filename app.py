import streamlit as st
import pandas as pd
import io
from generador_base import generar_carnet

def main():
    ### Sidebar (Formulario)
    st.sidebar.header("⚙️ Configuración")
    with st.sidebar.form(key="formulario_usuario", clear_on_submit=False):
        nombre = st.sidebar.text_input("Nombre Completo: ", key="nombre")
        cargo = st.sidebar.text_input("Cargo: ", key="cargo")
        empleado_id = st.sidebar.text_input("Número de Empleado: ", key="numero_empleado")

    st.sidebar.header("🎨 Estética")
    color_marca = st.sidebar.color_picker("Color de la Marca: ", "#0000ff")

    st.sidebar.header("📸 Multimedia")
    foto_subida = st.sidebar.file_uploader(
        "Foto",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )


    st.set_page_config(
        page_title="ID-Gen Pro",
        page_icon="📷",
        initial_sidebar_state="expanded",
    )

    main = st.container()
    with main:
        st.markdown("<h1 style='text-align: center; color: #ff0000'>🆔 ID-Gen Pro</h1>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'> <strong>Proyecto final:</strong> Generador de Identidad Corporativa</div>", unsafe_allow_html=True)
    
    st.markdown("---")

    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.header("Vista Previa")
        st.write("Aquí se mostrarán los datos ingresados por el usuario.")

        if foto_subida is not None:
            foto_bytes = io.BytesIO(foto_subida.read())
            imagen_buffer = generar_carnet(nombre, cargo, empleado_id, color_marca, foto_bytes)
            st.image(imagen_buffer, caption="Carnet Generado", use_container_width=True)
    with col2:
        st.header("Exportar")
        st.write("Verifica que los datos sean correctos. La imagen se descargará en formato PNG de alta resolución.")

        if foto_subida is not None:
            foto_bytes_dl   = io.BytesIO(foto_subida.getvalue())
            imagen_descarga = generar_carnet(nombre, cargo, empleado_id, color_marca, foto_bytes_dl)
            nombre_archivo  = f"carnet_{nombre.replace(' ', '_')}.png"

            st.download_button(
                    label="📥 Descargar Credencial",
                    data=imagen_descarga,
                    file_name=nombre_archivo,
                    mime="image/png",
                    use_container_width=True,
                    key="descargar",
                    type="primary"
                )

            with st.container(key="limpiar"):
                if st.button("✨ Limpiar Todo", use_container_width=True, key="limpiar_btn"):
                    st.rerun()
        else:
            st.warning("Sube una foto para habilitar la descarga.")

if __name__ == "__main__":
    main()